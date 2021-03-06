# Copyright (c) 2015, Vienna University of Technology,
# Department of Geodesy and Geoinformation
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the Vienna University of Technology,
#     Department of Geodesy and Geoinformation nor the
# names of its contributors may be used to endorse or promote products #
# derived from this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL VIENNA UNIVERSITY OF TECHNOLOGY,
# DEPARTMENT OF GEODESY AND GEOINFORMATION BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from __future__ import division

import pytesmo.metrics as met
import numpy as np

import numpy.testing as nptest


def test_pearson_conf():
    """
    Test the person confidence interval based on
    the fisher z-transform
    """
    # first example
    n = 34
    r = 0.654
    rl, ru = met.pearson_conf(r, n, c=95)
    nptest.assert_almost_equal(rl, 0.406, decimal=3)
    nptest.assert_almost_equal(ru, 0.812, decimal=3)

    rl, ru = met.pearson_conf(r, n, c=99)
    nptest.assert_almost_equal(rl, 0.309, decimal=3)
    nptest.assert_almost_equal(ru, 0.8468, decimal=3)

    # second example
    r = 0.824
    n = 300
    rl, ru = met.pearson_conf(r, n, c=95)
    nptest.assert_almost_equal(rl, 0.784, decimal=3)
    nptest.assert_almost_equal(ru, 0.857, decimal=3)

    rl, ru = met.pearson_conf(r, n, c=99)
    nptest.assert_almost_equal(rl, 0.7697, decimal=3)
    nptest.assert_almost_equal(ru, 0.866, decimal=3)

    # test numpy arrays as input

    r = np.array([0.654, 0.824])
    n = np.array([34, 300])
    rl, ru = met.pearson_conf(r, n, c=95)
    nptest.assert_almost_equal(rl, np.array([0.406, 0.784]), decimal=3)
    nptest.assert_almost_equal(ru, np.array([0.812, 0.857]), decimal=3)


def test_pearson_recursive():

    x = np.random.rand(100)
    y = np.random.rand(100)

    r, p = met.pearsonr(x, y)
    r_rec, _ = met.pearsonr_recursive(x, y)
    nptest.assert_almost_equal(r, r_rec)

    args = []
    for xi, yi in zip(x, y):

        r_rec, args = met.pearsonr_recursive(np.array([xi]),
                                             np.array([yi]), *args)

    nptest.assert_almost_equal(r, r_rec)


def test_bias():
    """
    Test for bias
    """
    # example 1
    x = np.arange(10)
    y = np.arange(10) + 2

    b_pred = -2
    b_obs = met.bias(x, y)

    nptest.assert_equal(b_obs, b_pred)

    # example 2
    x = np.arange(10)
    y = np.arange(20, 30)

    b_pred = 20.
    b_obs = met.bias(y, x)

    nptest.assert_equal(b_obs, b_pred)


def test_aad():
    """
    Test for average absolute deviation
    """
    # example 1
    x = np.arange(10)
    y = np.arange(10) + 2
    dev_pred = 2.
    dev_obs = met.aad(x, y)

    nptest.assert_equal(dev_obs, dev_pred)

    # example 2, with outlier
    x = np.arange(10)
    y = np.arange(10) + 2
    y[-1] = 201.
    dev_pred = 21.
    dev_obs = met.aad(x, y)

    nptest.assert_equal(dev_obs, dev_pred)


def test_mad():
    """
    Test for median absolute deviation
    """
    # example 1
    x = np.arange(10)
    y = np.arange(10) + 2
    dev_pred = 2.
    dev_obs = met.mad(x, y)

    nptest.assert_equal(dev_obs, dev_pred)

    # example 2, with outlier
    x = np.arange(10)
    y = np.arange(10) + 2
    y[-1] = 201.
    dev_pred = 2.
    dev_obs = met.mad(x, y)

    nptest.assert_equal(dev_obs, dev_pred)


def test_rmsd():
    """
    Test for rmsd
    """
    # example 1
    x = np.arange(10)
    y = np.arange(10) + 2

    rmsd_pred = 2.
    rmsd_obs = met.rmsd(x, y)

    nptest.assert_equal(rmsd_obs, rmsd_pred)

    # example 2, with outlier
    x = np.arange(10)
    y = np.arange(10) + 2
    y[-1] = 100.

    rmsd_pred = np.sqrt(831.7)
    rmsd_obs = met.rmsd(x, y)

    nptest.assert_almost_equal(rmsd_obs, rmsd_pred, 6)


def test_ubrmsd():
    """
    Test for ubrmsd
    """
    # example 1
    x = np.arange(10)
    y = np.arange(10) + 2

    ubrmsd_pred = 0
    ubrmsd_obs = met.ubrmsd(x, y)

    nptest.assert_equal(ubrmsd_obs, ubrmsd_pred)
    # aslo check consistency with direct formula
    ubrmsd_direct = np.sqrt(met.rmsd(x, y) ** 2 - met.bias(x, y)**2)
    nptest.assert_equal(ubrmsd_obs, ubrmsd_direct)

    # example 2, with outlier
    x = np.arange(10)
    y = np.arange(10) + 2
    y[-1] = 100.

    ubrmsd_pred = 26.7
    ubrmsd_obs = met.ubrmsd(x, y)

    nptest.assert_almost_equal(ubrmsd_obs, ubrmsd_pred, 6)
    # aslo check consistency with direct formula
    ubrmsd_direct = np.sqrt(met.rmsd(x, y) ** 2 - met.bias(x, y)**2)
    nptest.assert_almost_equal(ubrmsd_obs, ubrmsd_direct)


def test_mse():
    """
    Test for mse
    """
    # example 1
    x = np.arange(10)
    y = np.arange(10) + 2

    mse_pred = 4.
    mse_bias_pred = 2. ** 2
    mse_obs, _, mse_bias, _ = met.mse(x, y)

    nptest.assert_equal(mse_obs, mse_pred)
    nptest.assert_equal(mse_bias, mse_bias_pred)

    # example 2, with outlier
    x = np.arange(10)
    y = np.arange(10) + 2
    y[-1] = 51.

    mse_pred = 180.
    mse_bias_pred = 36.
    mse_obs, _, mse_bias, _ = met.mse(x, y)

    nptest.assert_almost_equal(mse_obs, mse_pred, 6)
    nptest.assert_almost_equal(mse_bias, mse_bias_pred, 6)


def test_rmsd_mse():
    """
    Test for rmsd and mse
    """
    # example 1
    x = np.random.randn(1000)
    y = np.random.randn(1000)

    rmsd_pred = met.rmsd(x, y)
    mse_pred, _, _, _ = met.mse(x, y)

    nptest.assert_almost_equal(rmsd_pred ** 2, mse_pred, 6)


def test_tcol_error():
    """
    Test the triple collocation error estimation based on
    a random signal and error.
    Also compare the results to the other method
    """

    n = 1000000

    signal = np.sin(np.linspace(0, 2 * np.pi, n))

    sig_err_x = 0.02
    sig_err_y = 0.07
    sig_err_z = 0.04
    err_pred = np.array((sig_err_x, sig_err_y, sig_err_z))
    err_x = np.random.normal(0, sig_err_x, n)
    err_y = np.random.normal(0, sig_err_y, n)
    err_z = np.random.normal(0, sig_err_z, n)

    alpha_y = 0.2
    alpha_z = 0.5

    beta_y = 0.9
    beta_z = 1.6

    x = signal + err_x
    y = alpha_y + beta_y * (signal + err_y)
    z = alpha_z + beta_z * (signal + err_z)

    snr, err, beta = met.tcol_snr(x, y, z, ref_ind=0)
    # classical triple collocation errors use scaled (removed alpha and beta)
    # input arrays
    ex, ey, ez = met.tcol_error(signal + err_x, signal + err_y, signal + err_z)

    nptest.assert_almost_equal(err, np.array([ex, ey, ez]), decimal=2)
    nptest.assert_almost_equal(err_pred, np.array([ex, ey, ez]), decimal=2)


def test_tcol_snr():
    """
    Test the triple collocation based estimation of
    signal to noise ratio, absolute errors and rescaling coefficients
    """

    n = 1000000

    mean_signal = 0.3
    sig_signal = 0.2
    signal = np.random.normal(mean_signal, sig_signal, n)

    sig_err_x = 0.02
    sig_err_y = 0.07
    sig_err_z = 0.04
    err_x = np.random.normal(0, sig_err_x, n)
    err_y = np.random.normal(0, sig_err_y, n)
    err_z = np.random.normal(0, sig_err_z, n)

    alpha_y = 0.2
    alpha_z = 0.5

    beta_y = 0.9
    beta_z = 1.6

    x = signal + err_x
    y = alpha_y + beta_y * (signal + err_y)
    z = alpha_z + beta_z * (signal + err_z)

    beta_pred = 1. / np.array((1, beta_y, beta_z))
    err_pred = np.array((sig_err_x, sig_err_y, sig_err_z))
    snr_pred = np.array(
        ((sig_signal / sig_err_x), (sig_signal / sig_err_y), (sig_signal / sig_err_z)))

    snr, err, beta = met.tcol_snr(x, y, z, ref_ind=0)

    nptest.assert_almost_equal(beta, beta_pred, decimal=2)
    nptest.assert_almost_equal(err, err_pred, decimal=2)
    nptest.assert_almost_equal(np.sqrt(10 ** (snr / 10.)), snr_pred, decimal=1)
