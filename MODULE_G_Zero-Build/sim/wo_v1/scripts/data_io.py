"""
§4.1 Load & resample + baseline removal.
Blinding rule: this module never touches annotations.
"""
from __future__ import annotations
import os
from pathlib import Path
from typing import Optional, Tuple
import numpy as np
from scipy.signal import butter, filtfilt, resample_poly
import wfdb
from config import TARGET_FS, HIGHPASS_CUTOFF, DATA_DIR

def ensure_data_dir() -> Path:
    p = Path(DATA_DIR)
    p.mkdir(parents=True, exist_ok=True)
    return p

def download_database(db_name: str, records: Optional[list] = None) -> Path:
    """Download PhysioNet database if not present. Returns local path."""
    data_root = ensure_data_dir()
    db_path = data_root / db_name
    db_path.mkdir(parents=True, exist_ok=True)
    
    need_download = False
    if records is None:
        if not any(db_path.iterdir()):
            need_download = True
    else:
        for rec in records:
            if not (db_path / f"{rec}.hea").exists():
                need_download = True
                break
                
    if need_download:
        print(f"Downloading {db_name} ...")
        try:
            if records is None:
                wfdb.dl_database(db_name, str(db_path))
            else:
                wfdb.dl_database(db_name, str(db_path), records=records)
        except Exception as e:
            print(f"Download warning: {e}")
            
    return db_path

def highpass_zero_phase(x: np.ndarray, fs: float, cutoff: float = HIGHPASS_CUTOFF) -> np.ndarray:
    """Zero-phase high-pass Butterworth (order 2) for baseline wander removal."""
    nyq = 0.5 * fs
    b, a = butter(2, cutoff / nyq, btype="high")
    return filtfilt(b, a, x)

def load_and_resample(
    db_name: str,
    record_name: str,
    channel: Optional[int] = None,
) -> Tuple[np.ndarray, float, dict]:
    """
    Load record, select first available ECG channel (or specified),
    resample to TARGET_FS with anti-aliasing, high-pass filter.
    Returns: signal (1-D float64), fs (TARGET_FS), meta dict.
    """
    db_path = download_database(db_name, records=[record_name])
    record_path = str(db_path / record_name)
    
    record = wfdb.rdrecord(record_path)
    original_fs = float(record.fs)
    sig = record.p_signal  # (n_samples, n_channels)
    
    if channel is None:
        channel = 0
        for i, name in enumerate(record.sig_name):
            n = name.upper()
            if "ECG" in n or n.startswith(("ML", "V", "II", "I")):
                channel = i
                break
    
    x = sig[:, channel].astype(np.float64)
    channel_name = record.sig_name[channel]
    
    if abs(original_fs - TARGET_FS) > 1e-6:
        from fractions import Fraction
        frac = Fraction(TARGET_FS / original_fs).limit_denominator(1000)
        up, down = frac.numerator, frac.denominator
        x = resample_poly(x, up, down)
        fs = TARGET_FS
    else:
        fs = original_fs
    
    x = highpass_zero_phase(x, fs)
    
    meta = {
        "db": db_name,
        "record": record_name,
        "channel_idx": channel,
        "channel_name": channel_name,
        "original_fs": original_fs,
        "fs": fs,
        "n_samples": len(x),
        "duration_s": len(x) / fs,
    }
    return x, fs, meta

def load_annotations(db_name: str, record_name: str) -> dict:
    """
    Load beat / arrhythmia / ischemia annotations.
    MUST be called only AFTER metrics are computed (blinding).
    """
    db_path = Path(DATA_DIR) / db_name
    record_path = str(db_path / record_name)
    try:
        ann = wfdb.rdann(record_path, "atr")  # standard for mitdb/nsrdb
        return {
            "sample": ann.sample.tolist(),
            "symbol": ann.symbol,
            "aux_note": getattr(ann, "aux_note", None),
            "fs": float(ann.fs) if hasattr(ann, "fs") else None,
        }
    except Exception:
        try:
            ann = wfdb.rdann(record_path, "sta")
            return {
                "sample": ann.sample.tolist(),
                "symbol": ann.symbol,
                "aux_note": getattr(ann, "aux_note", None),
                "fs": float(ann.fs) if hasattr(ann, "fs") else None,
            }
        except Exception as e:
            return {"error": str(e), "sample": [], "symbol": []}
