## Half-Life Weapon Sprites HUD Upscaler 

### Overview

The Half-Life 25th Anniversary update introduced support for higher screen resolutions. However, to properly display weapon sprites in the updated HUD, the associated `.spr` and `.txt` files must be updated. Without these updates, the sprites may appear distorted or misaligned.

This utility automates the process of generating updated `.spr` and `.txt` files, ensuring compatibility with the new resolution support and streamlining the workflow.

#### weapon_357.txt before 25th anniversary update 

```
12
weapon         320 320hud1   0   80   80   20
weapon_s      320 320hud1   0   100   80   20
ammo         320 320hud2   18   16   18   18
crosshair      320 crosshairs   48   0   24   24
autoaim         320 crosshairs   24   72   24   24
zoom         320 crosshairs   96   0   24   24
weapon         640 640hud1   0   90   170   45
weapon_s      640 640hud4   0   90   170   45
ammo         640 640hud7   24   72   24   24
crosshair      640 crosshairs   48   0   24   24
autoaim         640 crosshairs   24   72   24   24
zoom         640 crosshairs   96   0   24   24
```

#### weapon_357.txt after 25th anniversary update

```
24
weapon         2560 2560/weapon_357_weapon   0   0   510   135
weapon_s      2560 2560/weapon_357_weapon_s   0   0   510   135
ammo         2560 2560/weapon_357_ammo   0   0   72   72
crosshair      2560 2560crosshairs   144   0   72   72
autoaim         2560 2560crosshairs   72   216   72   72
zoom         2560 2560crosshairs   288   0   72   72
weapon         1280 1280/weapon_357_weapon   0   0   340   90
weapon_s      1280 1280/weapon_357_weapon_s   0   0   340   90
ammo         1280 1280/weapon_357_ammo   0   0   48   48
crosshair      1280 1280crosshairs   96   0   48   48
autoaim         1280 1280crosshairs   48   144   48   48
zoom         1280 1280crosshairs   192   0   48   48
weapon         640 640hud1   0   90   170   45
weapon_s      640 640hud4   0   90   170   45
ammo         640 640hud7   24   72   24   24
crosshair      640 crosshairs   48   0   24   24
autoaim         640 crosshairs   24   72   24   24
zoom         640 crosshairs   96   0   24   24
weapon         320 320hud1   0   80   80   20
weapon_s      320 320hud1   0   100   80   20
ammo         320 320hud2   18   16   18   18
crosshair      320 crosshairs   48   0   24   24
autoaim         320 crosshairs   24   72   24   24
zoom         320 crosshairs   96   0   24   24
```


---

### Environment Setup

Follow these steps to configure the environment for the utility:

1. Install **Python 3**.
2. Clone the repository or download the contents as a compressed archive and extract them.
3. Install the required Python packages by running:

   ```bash
   pip3 install -r requirements.txt
   ```
4. The utility can automatically use paths to the standard highres sprites for ammo and crosshairs added in the HL25th Anniversary Update (it will be done if your sprite uses their default versions in resolution 640). To avoid issues, make sure to add them to the server's precache.
5. Configuration is complete! You are now ready to use the utility.

---

### Usage Instructions

1. Place all the required `.spr` and `.txt` files in a **single directory** (see example below):

   ![Directory Structure](https://github.com/user-attachments/assets/736e3b68-8263-4fa8-80db-0803cf9b9305)

2. Run the utility using the following command:

   ```bash
   python3 hud_upscaler.py --path /path/to/directory/with/your/weapon/sprites --umodel edsr-base
   ```

#### Command Line Arguments:

- **`--path`**: The path to the directory containing your `.spr` and `.txt` files.
- **`--umodel`**: The name of the upscaling model to use.  
  You can find the list of available models [here](https://pypi.org/project/super-image/) or in the table below:

   ![Model List](https://github.com/user-attachments/assets/1d7f80ae-0e2c-44fc-ad7d-9359193497b3)

---

### Comparation 

#### Weaponmod gun before the utlity was used

![Before Update](https://github.com/user-attachments/assets/b6e0a7e4-c97e-4a2d-82e2-855199d7deb4)

#### Weaponmod gun after the utlity was used

![After Update](https://github.com/user-attachments/assets/d2a4cd4a-1d05-411f-bcf1-99a85c8c2971)

### Links 

- https://github.com/ValveSoftware/halflife/blob/master/devtools/image_to_spr.py
- https://developer.valvesoftware.com/wiki/SPR
- https://twhl.info/wiki/page/hud.txt_and_weapon_*.txt
- http://infotex58.ru/forum/index.php?topic=1135.0
- https://pypi.org/project/super-image/
