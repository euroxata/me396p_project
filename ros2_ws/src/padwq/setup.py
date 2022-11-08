import os
from glob import glob
from setuptools import setup

package_name = 'padwq'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name), glob('launch/*.launch.py')),
        (os.path.join('share', package_name), glob('launch/*.rviz')),
        (os.path.join('share', package_name), glob('urdf/*.urdf')),
        (os.path.join('share', package_name), glob('meshes/*.stl'))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Automatons',
    maintainer_email='automatons@not.there',
    description='Model of a PADWQ robot',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)