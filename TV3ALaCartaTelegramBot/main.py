from TelegramBot import TelegramBot
from os.path import exists
import time
import os

fileConfig="Config";

if exists(fileConfig):
    fConfig = open(fileConfig, "r");
    config = fConfig.readlines();
    fConfig.close();
    token=config[0];
elif len(args)>1:
    token=args[1];
    fConfig = open(fileConfig, 'w');
    fConfig.writelines([token]);
    fConfig.close();

TelegramBot.Start(token);
while True:
    time.sleep(60*60*1000);