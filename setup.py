from distutils.command.build_py import build_py
import os
from setuptools import setup


class GenerateBindings(build_py):
    os.system('echo generating bindings')
    os.system('protoc -I=proto-schema --python_out=kafka_proto_api/protos proto-schema/etf.proto')
    os.system('echo generated bindings')

setup(name='kafka_proto_py',
      version='0.0.1',
      description='',
      author='Yves',
      cmdclass={'build_py': GenerateBindings}
     )