## Half-Life Weapon Sprites HUD Upscaler 

### Overview

The Half-Life 25th Anniversary update introduced support for higher screen resolutions. However, to properly display weapon sprites in the updated HUD, the associated `.spr` and `.txt` files must be updated. Without these updates, the sprites may appear distorted or misaligned.

This utility automates the process of generating updated `.spr` and `.txt` files, ensuring compatibility with the new resolution support and streamlining the workflow.

#### Weapon Display Before Updating Sprites

![Before Update](https://github.com/user-attachments/assets/b6e0a7e4-c97e-4a2d-82e2-855199d7deb4)

#### Weapon Display After Updating Sprites

![After Update](https://github.com/user-attachments/assets/d2a4cd4a-1d05-411f-bcf1-99a85c8c2971)

---

### Environment Setup

Follow these steps to configure the environment for the utility:

1. Install **Python 3**.
2. Clone the repository or download the contents as a compressed archive and extract them.
3. Install the required Python packages by running:

   ```bash
   pip3 install -r requirements.txt
   ```

4. Configuration is complete! You are now ready to use the utility.

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

### Links 

- https://github.com/ValveSoftware/halflife/blob/master/devtools/image_to_spr.py
- https://developer.valvesoftware.com/wiki/SPR
- https://twhl.info/wiki/page/hud.txt_and_weapon_*.txt
- http://infotex58.ru/forum/index.php?topic=1135.0
- https://pypi.org/project/super-image/
