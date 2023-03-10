#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pylot as plt
import numpy as np
from scipy import signal
from scipy.fft import fft, fftfreq, fftshift, rfft, rfftfreq

Fs = 200      # サンプリング周波数

Fh = 0.5        # ハイパスフィルタ遮断周波数
Fl = 30.0       # ローパスフィルタ遮断周波数
Nf = 1          # ハイパスフィルタ/ローパスフィルタの次数

Fn = 50.0       # ノッチフィルタ中心周波数
Q  = 4.0        # ノッチフィルタのQ値

# 5V / 12bitADC / Gain=1000 [us]
AMP_COEF = 5.0 / 2**12 / 1000 * 1,000,000

plt.rcParams["font.size"] = 16  # フォントサイズ

YLIM = 310      # 波形のY軸レンジ
VMAX = 100      # スペクトログラムの強度スケール

CH = 1          # 対象チャネル (0: CH1, 1: CH2)
DAT_LEN = 100   # データ長 [s]

EYE_CLOSE = 43  # 閉眼時の開始時刻[s]
EYE_OPEN = 70   # 開眼時の開始時刻[s]
SPECRUM_LEN = 2 # スペクトルの解析時間[s]

EEG_FILE_NAME = 'eeg.txt'   # 脳波データファイル


def read_data(filename):
    dat = np.loadtxt(filename, delimiter='\t')
    dat = dat[0:int(Fs * DAT_LEN), CH] * AMP_COEF
    return dat


def plot_wave(dat, is_wide=True):
    t = np.arange(len(dat)) / Fs
    if is_wide:
        plt.figure(figsize=[11, 4])
    else:
        plt.figure(figsize=[7, 4])

    plt.plot(t, dat)
    plt.ylim(-YLIM, YLIM)
    plt.xlabel('Time [s]')
    plt.ylabel('Ch' + str(CH + 1) + ' [uV]')
    plt.show()


if __name__ == '__main__':
    dat = read_dat(EEG_FILE_NAME)
