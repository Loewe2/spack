# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install octotiger-git
#
# You can edit this file again by typing:
#
#     spack edit octotiger-git
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class OctotigerGit(CMakePackage, CudaPackage):
    """Octo-Tiger is an astrophysics program simulating the evolution of star systems based on the fast multipole method on adaptive Octrees.
    It was implemented using high-level C++ libraries, specifically HPX and Vc, which allows its use on different hardware platforms."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    url      = "https://github.com/STEllAR-GROUP/octotiger.git"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    maintainers = ['Loewe2']

    # FIXME: Add proper versions and checksums here.
    version('master', git='https://github.com/STEllAR-GROUP/octotiger.git', branch='master')

    # FIXME: Add dependencies if required.
    depends_on('cmake@3.13.2')
    depends_on('boost@1.68.0 cxxstd=17')
    depends_on('gcc@7.3.0')
    depends_on('cuda')
    depends_on('hdf5@1.8.12')
    depends_on('silo') #Todo: version 4.10.12
    # depends_on('jemalloc')
    depends_on('hwloc@1.11.12')
    depends_on('vc@1.4.1')
    depends_on('hpx@1.4.0+cuda')
    depends_on('gperftools')
    depends_on('zlib')


    variant('cxxstd',
            default='17',
            values=('11', '14', '17'),
            description='Use the specified C++ standard when building.')



    def cxx_standard(self):
        value = self.spec.variants['cxxstd'].value
        return '-DCMAKE_CXX_STANDARD={0}'.format(value)
  
    def cmake_args(self):
        spec, args = self.spec, []

        # CXX Standard
        args.append(self.cxx_standard())

        args.extend([
            '-DHPX_DIR={0}'.format(spec['hpx'].prefix),
            '-DSilo_DIR={0}'.format(spec['silo'].prefix),
            '-DHDF5_ROOT={0}'.format(spec['hdf5'].prefix),
            '-DBOOST_ROOT={0}'.format(spec['boost'].prefix),
            '-DHPX_WITH_BOOST_ALL_DYNAMIC_LINK=ON',
            '-DOCTOTIGER_WITH_BLAST_TEST=OFF',
            '-DOCTOTIGER_WITH_TEST=OFF',
            '-DCMAKE_BUILD_TYPE=RelWithDebInfo',
            '-DOCTOTIGER_WITH_CUDA=ON',
            '-DOCTOTIGER_WITH_SILO=ON',
            '-DCUDA_NVCC_FLAGS=-Xcompiler=-fPIC'
        ])

        return args
