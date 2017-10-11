import os
import numpy
from scipy.interpolate import InterpolatedUnivariateSpline as spline

class eBOSSConfig(object):
    """
    Configuration class for the eBOSS results + fits

    Parameters
    ----------
    sample : 'N', 'S'
        the eBOSS sample we are fitting
    version : str
        the version we are fitting
    """
    def __init__(self, sample, version):

        assert sample in ['N', 'S']
        self.version = version
        self.sample = sample

    def _get_nbar_file(self):
        filename = f'nbar-eboss_{self.version}-QSO-{self.sample}-eboss_{self.version}.dat'
        return os.path.join(self.data_dir, 'meta', filename)

    def _get_effective_area(self):
        """
        Return the effective area in squared degrees from the relevant nbar file.
        """
        f = self._get_nbar_file()
        lines = open(f, 'r').readlines()
        return float(lines[1].split()[0])

    def _get_nbar(self):
        """
        Return a spline fit to n(z).
        """
        f = self._get_nbar_file()
        nbar = numpy.loadtxt(f, skiprows=3)
        return spline(nbar[:,0], nbar[:,3])

    @property
    def home_dir(self):
        return os.path.join(os.environ['THESIS_DIR'], 'eBOSS-QSO-PNG')

    @property
    def fits_input_dir(self):
        return os.path.join(os.environ['THESIS_DIR'], 'eBOSS-QSO-PNG', 'fits', 'input')

    @property
    def fits_covariance_dir(self):
        return os.path.join(self.fits_input_dir, 'covariance', self.version)

    @property
    def fits_window_dir(self):
        return os.path.join(self.fits_input_dir, 'window', self.version)

    @property
    def fits_data_dir(self):
        return os.path.join(self.fits_input_dir, 'data', self.version)

    @property
    def fits_params_dir(self):
        return os.path.join(self.fits_input_dir, 'params')

    @property
    def fits_results_dir(self):
        return os.path.join(os.environ['THESIS_DIR'], 'eBOSS-QSO-PNG', 'fits', 'results', self.version)

    @property
    def spectra_dir(self):
        return os.path.join(self.home_dir, 'measurements', 'spectra')

    @property
    def data_dir(self):
        return os.path.join(self.home_dir, 'data', self.version)

    @property
    def fsky(self):
        try:
            return self._fsky
        except AttributeError:
            eff_area = self._get_effective_area()
            self._fsky = eff_area * (numpy.pi/180.)**2 / (4*numpy.pi)
            return self._fsky

    @property
    def nbar(self):
        try:
            return self._nbar
        except AttributeError:
            self._nbar = self._get_nbar()
            return self._nbar

    @property
    def cosmo(self):
        from ..measurements import fidcosmo
        return fidcosmo


from .runner import RSDFitRunner