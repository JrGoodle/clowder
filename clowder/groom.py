import sys
import os
import shutil
import subprocess

import ev.config
import ev.log
import ev.utilities

def groom():
    if arg1 == 'core':
        genCmakeCore(arg2)
    elif arg1 == 'opencv':
        genCmakeOpenCV(arg2)
    else:
        ev.utilities.unknownArg('ev cmake', arg1)
    return

def genCmakeCore(plat):
    d = ev.config.load()
    if plat == '':
        plat = d['EVPLATFORM']
    gen = d['EV_GENERATOR']
    ed = d['EVDIR']
    name = 'core/' + plat

    if gen == 'Unix Makefiles':
        genPrefix = 'make'
    elif gen == 'Ninja':
        genPrefix = 'ninja'
    elif gen == 'Xcode':
        genPrefix = 'xcode'
    else:
        ev.log.toFile('Unknown generator: ' + gen)
        ev.log.toFile('Aborting.\n\n')
        sys.exit()

    if plat == 'linux':
        p = 'Linux'
    elif plat == 'osx':
        p = 'OSX'
    elif plat == 'android':
        p = 'Android'
    else:
        ev.log.toFile('Unknown plat for generating cmake core: ' + plat)
        ev.log.toFile('Aborting.\n\n')
        sys.exit()

    ev.log.toFile('Generating core built trees for {} with the {} generator...'.format(p, gen))

    libType = ['shared', 'static']
    buildType = ['debug', 'release', 'relwithdebinfo', 'minsizerel']

    if plat == 'osx' or plat == 'linux':
        for bt in buildType:
            for lt in libType:
                if lt == 'static' or lt == 'Static':
                    shared = 'OFF'
                elif lt == 'shared' or lt == 'Shared':
                    shared = 'ON'
                else:
                    ev.log.toFile('Unknown Library Type: ' + lt)
                    ev.log.toFile('Aborting.\n\n')
                    sys.exit()

                buildDir = '{0}/build/{1}/{2}-{3}-{4}'.format(ed, name, genPrefix, lt, bt)
                if os.path.exists(buildDir):
                    shutil.rmtree(buildDir)
                os.makedirs(buildDir)
                cwd = os.getcwd()
                os.chdir(buildDir)
                c = 'export OPENCV_DIR="{0}/share/OPENCV" && '.format(d['OPENCV_DIR'])
                c = 'cmake -G"{0}" -Wno-dev '.format(gen)
                c += '-DCMAKE_BUILD_TYPE="{0}" '.format(bt)
                c += '-DBUILD_SHARED_LIBS="{0}" '.format(shared)
                c += '-DOpenCV_DIR="{0}/share/OPENCV" '.format(d['OPENCV_DIR'])
                c += '-DCMAKE_INSTALL_PREFIX="{0}/install" "{0}"'.format(ed)
                ev.utilities.ex(c)
                os.chdir(cwd)

    elif plat == 'android':
        cmakeATC = ed + '/share/opencv/platforms/android/android.toolchain.cmake'

        cpuArch = ['arm', 'aarch64', 'x86', 'x86_64']
        for arch in cpuArch:
            for bt in buildType:
                for lt in libType:
                    if lt == 'static' or lt == 'Static':
                        shared = 'OFF'
                    elif lt == 'shared' or lt == 'Shared':
                        shared = 'ON'
                    else:
                        ev.log.toFile('Unknown Library Type: ' + lt)
                        ev.log.toFile('Aborting.\n\n')
                        sys.exit()

                    if arch == 'arm':
                        atcName ='arm-linux-androideabi-clang3.5'
                        abi = 'armeabi-v7a with NEON'
                        nativeLvl = 'android-16'
                        forceArmBuild = 'ON'
                    elif arch == 'aarch64':
                        atcName ='aarch64-linux-android-4.9'
                        abi = 'arm64-v8a'
                        nativeLvl = 'android-21'
                        forceArmBuild = 'OFF'
                    elif arch == 'x86':
                        atcName ='x86-clang3.5'
                        abi = 'x86'
                        nativeLvl = 'android-16'
                        forceArmBuild = 'OFF'
                    elif arch == 'x86_64':
                        atcName ='x86_64-4.9'
                        abi = 'x86_64'
                        nativeLvl = 'android-21'
                        forceArmBuild = 'OFF'
                    else:
                        ev.log.toFile('Unknown android architecture: ' + arch)
                        ev.log.toFile('Aborting\n\n')
                        sys.exit()

                    buildDir = '{0}/build/{1}/{2}-{3}-{4}-{5}'.format(ed, name, genPrefix, arch, lt, bt)
                    if os.path.exists(buildDir):
                        shutil.rmtree(buildDir)
                    os.makedirs(buildDir)
                    cwd = os.getcwd()
                    os.chdir(buildDir)
                    c = 'export CMAKE_ANDROID_TOOLCHAIN="{0}" && '.format(cmakeATC)
                    c += 'export ANDROID_NDK="{0}" && '.format(d['NDK_ROOT'])
                    c += 'cmake -G"{0}" -Wno-dev '.format(gen)
                    c += '-DANDROID_STL="gnustl_static" '
                    c += '-DANDROID_STL_FORCE_FEATURES="ON" '
                    c += '-DANDROID_TOOLCHAIN_NAME="{0}" '.format(atcName)
                    c += '-DANDROID_ABI="{0}" '.format(abi)
                    c += '-DANDROID_NATIVE_API_LEVEL="{0}" '.format(nativeLvl)
                    c += '-DANDROID_FORCE_ARM_BUILD="{0}" '.format(forceArmBuild)
                    c += '-DOpenCV_DIR="{0}/prebuilts/android/opencv/sdk/native/jni" '.format(ed)
                    c += '-DBUILD_SHARED_LIBS="{0}" '.format(shared)
                    c += '-DCMAKE_TOOLCHAIN_FILE="{0}" '.format(cmakeATC)
                    c += '-DCMAKE_BUILD_TYPE="{0}" '.format(bt)
                    c += '-DLIBRARY_OUTPUT_PATH_ROOT="'
                    c += '{0}/build/{1}/output" '.format(ed, name)
                    c += '-DCMAKE_INSTALL_PREFIX="'
                    c += '{0}/build/{1}/install" "{0}"'.format(ed, name)
                    ev.utilities.ex(c)
                    os.chdir(cwd)
    return

def genCmakeOpenCV(plat):
    d = ev.config.load()
    gen = d['EV_GENERATOR']
    ed = d['EVDIR']
    name = 'opencv/' + plat
    opencvRoot = ed + '/share/opencv'

    if gen == 'Unix Makefiles':
        genPrefix = 'make'
    elif gen == 'Ninja':
        genPrefix = 'ninja'
    elif gen == 'Xcode':
        genPrefix = 'xcode'
    else:
        ev.log.toFile('Unknown generator: ' + gen)
        ev.log.toFile('Aborting.\n\n')
        sys.exit()

    if plat == 'linux':
        p = 'Linux'
    elif plat == 'osx':
        p = 'OSX'
    elif plat == 'android':
        p = 'Android'
    else:
        ev.log.toFile('Unknown plat for genrating cmake opencv: ' + plat)
        ev.log.toFile('Aborting.\n\n')
        sys.exit()

    ev.log.toFile('Generating OpenCV built trees for {0} with the {1} generator...'.format(p, gen))

    bt = 'release'
    lt = 'static'

    if plat == 'osx' or plat == 'linux':
        if lt == 'static':
            shared = 'OFF'
        elif lt == 'shared':
            shared = 'ON'
        else:
            ev.log.toFile('Unknown Library Type: ' + lt)
            ev.log.toFile('Aborting.\n\n')
            sys.exit()

        buildDir = '{0}/build/{1}/{2}-{3}-{4}'.format(ed, name, genPrefix, lt, bt)
        if os.path.exists(buildDir):
            shutil.rmtree(buildDir)
        os.makedirs(buildDir)
        cwd = os.getcwd()
        os.chdir(buildDir)
        c = 'cmake -G"{0}" -Wno-dev '.format(gen)
        c += '-DCMAKE_BUILD_TYPE="{0}" '.format(bt)
        c += '-DBUILD_SHARED_LIBS="{0}" '.format(lt)
        c += '-DCMAKE_INSTALL_PREFIX="{0}/prebuilds/{1}/opencv" '.format(ed, plat)
        c += '-DOPENCV_EXTRA_MODULES_PATH="{0}/share/opencv_contrib/modules" '.format(ed)
        c += '-C "{0}/cmake/ConfigureOpenCV-{1}.cmake" "{2}"'.format(ed, p, opencvRoot)
        ev.utilities.ex(c)
        os.chdir(cwd)

    elif plat == 'android':
        opencvAndroidCmakeDir = '{0}/share/opencv/platforms/android'.format(ed)
        cmakeATC = ed + '/share/opencv/platforms/android/android.toolchain.cmake'

        cpuArch = ['arm', 'aarch64', 'x86', 'x86_64']
        for arch in cpuArch:
            if lt == 'static':
                shared = 'OFF'
            elif lt == 'shared':
                shared = 'ON'
            else:
                ev.log.toFile('Unknown Library Type: ' + lt)
                ev.log.toFile('Aborting.\n\n')
                sys.exit()

            if arch == 'arm':
                atcName ='arm-linux-androideabi-clang3.5'
                abi = 'armeabi-v7a with NEON'
                nativeLvl = 'android-16'
                forceArmBuild = 'ON'
            elif arch == 'aarch64':
                atcName ='aarch64-linux-android-4.9'
                abi = 'arm64-v8a'
                nativeLvl = 'android-21'
                forceArmBuild = 'ON'
            elif arch == 'x86':
                atcName ='x86-clang3.5'
                abi = 'x86'
                nativeLvl = 'android-16'
                forceArmBuild = 'OFF'
            elif arch == 'x86_64':
                atcName ='x86_64-4.9'
                abi = 'x86_64'
                nativeLvl = 'android-21'
                forceArmBuild = 'OFF'
            else:
                ev.log.toFile('Unknown android architecture: ' + arch)
                ev.log.toFile('Aborting\n\n')
                sys.exit()

            buildDir = '{0}/build/{1}/{2}-{3}-{4}-{5}'.format(ed, name, genPrefix, arch, lt, bt)
            if os.path.exists(buildDir):
                shutil.rmtree(buildDir)
            os.makedirs(buildDir)
            cwd = os.getcwd()
            os.chdir(buildDir)
            c = 'export ANDROID_NDK="{0}" && '.format(d['NDK_ROOT'])
            c += 'cmake -G"{0}" -Wno-dev '.format(gen)
            c += '-DANDROID_FORCE_ARM_BUILD="{0}" '.format(forceArmBuild)
            c += '-DANDROID_STL="gnustl_static" '
            c += '-DANDROID_STL_FORCE_FEATURES="ON" '
            c += '-DANDROID_TOOLCHAIN_NAME="{0}" '.format(atcName)
            c += '-DANDROID_ABI="{0}" '.format(abi)
            c += '-DANDROID_NATIVE_API_LEVEL="{0}" '.format(nativeLvl)
            c += '-DBUILD_SHARED_LIBS="{0}" '.format(shared)
            c += '-DCMAKE_BUILD_TYPE="{0}" '.format(bt)
            c += '-DCMAKE_TOOLCHAIN_FILE="{0}" '.format(cmakeATC)
            c += '-DCMAKE_INSTALL_PREFIX="'
            c += '{0}/prebuilts/android/opencv" '.format(ed)
            c += '-DOPENCV_EXTRA_MODULES_PATH="'
            c += '{0}/share/opencv_contrib/modules" '.format(ed)
            c += '-C "{0}/cmake/ConfigureOpenCV-Android.cmake" '.format(ed)
            c += '"{0}"'.format(opencvRoot)
            ev.utilities.ex(c)
            os.chdir(cwd)
    return
