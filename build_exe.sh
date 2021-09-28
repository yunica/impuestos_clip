pyinstaller  --onefile  --clean --name impuesto.bin setup.py
docker run --rm -v  "$(pwd):/src/" cdrx/pyinstaller-windows

