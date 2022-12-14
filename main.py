
# Copyright (c) 2021 brainlife.io
#
# This file is a MNE python-based brainlife.io App
#


# set up environment
import os
import json
import mne
import numpy as np
import pandas as pd

import matplotlib.image

import matplotlib.pyplot as plt

#workaround for -- _tkinter.TclError: invalid command name ".!canvas"
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


# Current path
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Load brainlife config.json
with open('config.json','r') as config_f:
    config = json.load(config_f)

# == LOAD DATA ==
fname = config['fif']
raw = mne.io.read_raw_fif(fname, verbose=False)

# eog_projs, eog_events = mne.preprocessing.compute_proj_eog(raw, n_grad=1, n_mag=1,
#                                                          n_eeg=1, average=True)

eog_projs, eog_events = mne.preprocessing.compute_proj_eog(raw, n_grad=config['n_grad'], n_mag=config['n_mag'],
                                                         n_eeg=config['n_eeg'], average=config['average'])



# eog_projs, eog_events = mne.preprocessing.compute_proj_eog(raw, None, config['tmin'], config['tmax'],
#                                    config['n_grad'], config['n_mag'], config['n_eeg'], config['l_freq'],
#                                    config['h_freq'], config['average'], config['filter_length'], None,
#                                    None, None, [], config['avg_ref'], config['no_proj'], config['event_id'],
#                                    config['eog_l_freq'], config['eog_h_freq'], config['tstart'],
#                                    config['filter_method'], None, None, config['copy'],
#                                    config['return_drop_log'], config['meg'])

# eog_projs, eog_events = mne.preprocessing.compute_proj_eog(raw, None, config['tmin'], config['tmax'], config['n_grad'],
#             config['n_mag'], config['n_eeg'], config['l_freq'], config['h_freq'], config['average'], config['filter_length'], None, None, None, None, [],
#             config['avg_ref'], config['no_proj'], config['event_id'], config['ecg_l_freq'], config['ecg_h_freq'], config['tstart'],
#             config['qrs_threshold'], config['filter_method'], None, config['copy'], config['return_drop_log'], config['meg'])


mne.write_proj('out_dir/proj.fif', eog_projs, overwrite=True)

# == FIGURES ==
plt.figure(1)
fig_ep = mne.viz.plot_projs_topomap(eog_projs, info=raw.info)
fig_ep.savefig(os.path.join('out_figs','eog_projectors.png'))


eog_evoked = mne.preprocessing.create_eog_epochs(raw).average()
eog_evoked.apply_baseline((None, None))

plt.figure(2)
e=eog_evoked.plot_joint(picks='mag')
e.savefig(os.path.join('out_figs','meg.png'))

plt.figure(3)
e=eog_evoked.plot_joint(picks='grad')
e.savefig(os.path.join('out_figs','grad.png'))

plt.figure(4)
e=eog_evoked.plot_joint(picks='eeg')
e.savefig(os.path.join('out_figs','eeg.png'))

