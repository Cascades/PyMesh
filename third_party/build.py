#!/usr/bin/env python

""" Build and install third party dependencies for PyMesh.
"""

import argparse
import subprocess
import os
import os.path
import tempfile
import shutil
import sys

def get_third_party_dependencies():
    return ["cgal", "mpir", "cork", "eigen",
        "tetgen", "triangle", "qhull", "clipper", "draco",
        "tbb", "mmg", "json"]

def parse_args():
    parser = argparse.ArgumentParser(__doc__);
    parser.add_argument("--cleanup", action="store_true",
            help="Clean up the build folder after done.");
    parser.add_argument("package",
            choices=["all"] + get_third_party_dependencies());
    return parser.parse_args();

def get_pymesh_dir():
    return os.path.join(sys.path[0], "..");

def build_generic(libname, build_flags="", cleanup=True):
    root_libname = os.path.normpath(libname)
    root_libname = root_libname.split("/")[0]
    pymesh_dir = get_pymesh_dir();
    build_dir = os.path.join(pymesh_dir, "third_party", "build", root_libname);
    if not os.path.exists(build_dir):
        os.makedirs(build_dir);
    
    arg0 = os.path.join(pymesh_dir, 'third_party', libname)
    arg1 = os.path.join(pymesh_dir, 'python', 'pymesh', 'third_party')

    # Configure cgal
    cmd = "cmake" + \
            " {}".format(arg0) + \
            " -DCMAKE_BUILD_TYPE=Release" + \
            " -DBUILD_SHARED_LIBS=Off" + \
            " -DCMAKE_POSITION_INDEPENDENT_CODE=On" + \
            build_flags + \
            " -DCMAKE_INSTALL_PREFIX={}".format(arg1);
    print("|_Configuring: " + cmd)
    subprocess.check_call(cmd.split(), cwd=build_dir);

    # Build cgal
    cmd = "cmake --build {}".format(build_dir);
    print("|_Building: " + cmd)
    subprocess.check_call(cmd.split());

    cmd = "cmake --install {}".format(build_dir);
    print("|_Installing: " + cmd)
    subprocess.check_call(cmd.split());

    # Clean up
    if cleanup:
        shutil.rmtree(build_dir)

def build(package, cleanup):
    print("Building " + str(package) + "...")
    if package == "all":
        for libname in get_third_party_dependencies():
            build(libname, cleanup);
    elif package == "cgal":
        build_generic("cgal",
                " -DWITH_CGAL_ImageIO=Off -DWITH_CGAL_Qt5=Off -DCGAL_DISABLE_GMP=On",
                cleanup=cleanup);
    elif package == "clipper":
        build_generic("Clipper/cpp", cleanup=cleanup);
    elif package == "tbb":
        build_generic("tbb",
                " -DTBB_BUILD_SHARED=On -DTBB_BUILD_STATIC=Off",
                cleanup=cleanup);
    elif package == "json":
        build_generic("json",
                " -DJSON_BuildTests=Off",
                cleanup=cleanup);
    elif package == "mpir":
        if os.name != "nt":
            return
        build_generic("mpir/msvc/vs22",
                cleanup=cleanup);
    else:
        build_generic(package, cleanup=cleanup);

def main():
    args = parse_args();
    build(args.package, args.cleanup);

if __name__ == "__main__":
    main();
