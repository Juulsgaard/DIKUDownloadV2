python setup.py bdist_wheel

rmdir build /S /Q
rmdir diku_tools.egg-info /S /Q

twine upload dist/* -u juulsgaard -p "%%F!0Oc&Ex%%r7K8H68APv"

cd dist
for /r %%i in (*) do pip install %%i -U
cd ..

rmdir dist /S /Q
exit