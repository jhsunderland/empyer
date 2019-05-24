from unittest import TestCase
import numpy as np

from hyperspy.signals import Signal2D, BaseSignal
from empyer.signals.diffraction_signal import DiffractionSignal


class TestDiffractionSignal(TestCase):
    def setUp(self):
        d = np.random.rand(10, 512, 512)
        self.center = [256, 256]
        self.lengths = sorted(np.random.rand(2) * 100 + 100, reverse=True)
        self.angle = np.random.rand() * np.pi
        rand_angle = np.random.rand(1000) * 2 * np.pi

        rand_points = [[(np.cos(ang) * self.lengths[0]), np.sin(ang) * self.lengths[1]] for ang in rand_angle]
        rand_points = np.array([[int(point[0] * np.cos(self.angle) - point[1] * np.sin(self.angle) + self.center[0]),
                                 int(point[1] * np.cos(self.angle) + point[0] * np.sin(self.angle) + self.center[1])]
                                for point in rand_points])
        d[:, rand_points[:, 0], rand_points[:, 1]] = 100
        d = np.random.poisson(d)

        self.bs = BaseSignal(data=d, lazy=True)
        self.s = Signal2D(self.bs)
        self.ds = DiffractionSignal(self.s)

    def test_ellipse(self):
        self.ds.determine_ellipse()
        self.assertAlmostEqual(self.ds.metadata.Signal.Ellipticity.center[0], self.center[0], places=-1)
        self.assertAlmostEqual(self.ds.metadata.Signal.Ellipticity.center[1], self.center[1], places=-1)
        self.assertAlmostEqual(self.ds.metadata.Signal.Ellipticity.lengths[0], max(self.lengths), places=-1)
        self.assertAlmostEqual(self.ds.metadata.Signal.Ellipticity.lengths[1], min(self.lengths), places=-1)
        self.assertAlmostEqual(self.ds.metadata.Signal.Ellipticity.angle, self.angle, places=1)

    def test_conversion(self):
        self.ds.calculate_polar_spectrum(phase_width=720,
                                         radius=None,
                                         parallel=False,
                                         inplace=False)

    def test_parallel_conversion(self):
        self.ds.calculate_polar_spectrum(phase_width=720,
                                         radius=None,
                                         parallel=True,
                                         inplace=False)

    def test_conversion_and_mask(self):
        self.ds.mask_slice(242, 262, 0, 512)
        ps = self.ds.calculate_polar_spectrum(phase_width=720,
                                              radius=None,
                                              parallel=False,
                                              inplace=False)
        ps.plot()
        ps.show_mask()
        ac = ps.autocorrelation()
        ac.plot()
        self.ds.show_mask()


