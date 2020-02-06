__all__ = ['write_stats']

import os
import pandas as pd


def write_stats(file_path, degradation=0, **stats):
    """Writes stats to a parquet file according to specified dict.

    If specified filepath exists already, appends. Otherwise creates
    new file and writes to it.

    Args:
        file_path: string designated output filepath
        stats: dict in form {'stat': value}
    """
    saved_stats = None
    if os.path.exists(file_path):
        saved_stats = pd.read_csv(file_path, header=0)

    stats['degradation'] = degradation
    new_stats = pd.DataFrame(data=[stats])
    if saved_stats is not None:
        saved_stats = saved_stats.append(new_stats, ignore_index=True)
    else:
        saved_stats = new_stats
    saved_stats.to_csv(file_path, index=False)
