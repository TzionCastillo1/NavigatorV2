from setuptools import setup

package_name = 'navigator'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Tzion Castillo',
    maintainer_email='tzcastillo@unm.edu',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'autopilot_interface = navigator.autopilot_node:main',
            'data_handler = navigator.data_handler:main',
        ],
    },
)
