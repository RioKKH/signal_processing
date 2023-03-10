#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from scipy.fft import fft, fftfreq, fftshift, rfft, rfftfreq

# バターワースフィルター
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

# バターワースフィルタの設計
# $1 N: フィルタ次数
# $2 Wn: 遮断（カットオフ）周波数 (fsと同じ単位にする)
# $3 btype: フィルタの種類
# $4 fs: サンプリング周波数
bh, ah = signal.butter(Nf, Fh, 'high', fs=Fs) # ハイパスフィルタ
bl, al = signal.butter(Nf, Fl, 'low', fs=Fs)   # ローパスフィルタ

# ノッチフィルタの設計
# $1 w0: 遮断(カットオフ)周波数 (fsと同じ単位にする)
# $2 Q: Q値
# $3 fs: サンプリング周波数
bn, an = signal.iirnotch(Fn, Q, fs=Fs)


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


def plot_freqz(b, a, title = '0.5Hz 1st butterworth HPF'):
    w, h = signal.freqz(b, a, worN = np.logspace(-2, 2, 512), fs=Fs)
    plt.figure()
    plt.subplot(211)
    plt.semilogx(w, 20 * np.log10(np.abs(h)))
    plt.ylim(-45, 5)
    plt.ylabel('Magnitude [dB]')
    plt.title(title)
    plt.grid(which='both', axis='both')

    plt.subplot(212)
    plt.semilogx(w, np.angle(h))
    plt.ylabel('Phase [Rad]')
    plt.xlabel('Frequency [Hz]')
    plt.grid(which='both', axis='both')
    plt.suptitle('Frequency response')
    plt.show()

if __name__ == '__main__':
    Fs = 200 # サンプリング周波数
    Fh - 0.5 # ハイパスフィルタ遮断周波数
    Nf = 1   # フィルタ次数

    #bh, ah = signal.butter(Nf, Fh, 'high', fs=Fs) 
    #plot_freqz(bh, ah)

    # 生波形
    dat = read_dat(EEG_FILE_NAME)
    plot_all(dat)
