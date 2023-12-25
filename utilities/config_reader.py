from environs import Env

env = Env()
env.read_env()

WORK_DIR = env.str("WORK_DIR")  # Забираем значение типа str

DSP_PCHO_DIR = env.str("DSP_PCHO_DIR")
DSP_TEZIS_DIR = env.str("DSP_TEZIS_DIR")
MEDO_DIR = env.str("MEDO_DIR")
SED_DIR = env.str("SED_DIR")

DSP_ID = env.str("DSP_ID")
PCHO_ID = env.str("PCHO_ID")