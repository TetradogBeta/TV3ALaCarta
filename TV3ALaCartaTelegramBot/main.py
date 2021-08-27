from TelegramBot import TelegramBot
from os.path import exists
import time
import os
import sys

fileConfig="Config";

if exists(fileConfig):
    fConfig = open(fileConfig, "r");
    config = fConfig.readlines();
    fConfig.close();
    token=config[0];
elif len(sys.argv)>1:
    token=args[1];
    fConfig = open(fileConfig, 'w');
    fConfig.writelines([token]);
    fConfig.close();
print("Iniciando TV3 A La Carta BOT v1.0")
TelegramBot.Start(token).run_forever();
