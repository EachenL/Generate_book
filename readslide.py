import os
if hasattr(os, 'add_dll_directory'):
    # Python >= 3.8 on Windows
    with os.add_dll_directory(os.getenv('OPENSLIDE_PATH')):
        import openslide
else:
    import openslide
p = openslide.OpenSlide(r'D:\slidedata\1-50\02585_1_SCC_1.ndpi')