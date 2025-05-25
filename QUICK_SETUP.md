# 🚀 Quick Setup Guide for Picosystem Platform Game

## Using VSCode wiht MicroPico Extension

1. **Enter USB Mode**:
   - Connect Picosystem to computer with USB-C cable
   - Turn the Picosystem on, it will show in the terminal in VSCode.

2. **Copy Game**:
   - In VSCode right click on the file you want to run on PicoSystem, select Run current file on pico.
   - When it is working the way you want it to, select Upload file to Pico, it will now start when you start your picoSystem automatically.

3. **Play**:
   - Restart your Picosystem
   - Game starts automatically!

## Controls
- **Arrow Keys**: Move left/right
- **A Button**: Jump
- **X Button**: Restart level

---

## Troubleshooting

❌ **"Device not found"**
- Try different USB port
- Make sure Picosystem is on
- On Windows: Install Pico drivers

❌ **Game doesn't start**
- File must be named exactly `main.py`
- Press reset button on Picosystem
- Check file uploaded completely

❌ **"Import Error"**
- Update Picosystem firmware
- Verify `picosystem` module exists

---

## What You Should See

✅ Blue player character
✅ Brown platforms to jump on
✅ Yellow collectibles that bob up and down
✅ Score in top-left corner
✅ Responsive controls

## Quick Customizations

**Make player red:**
```python
# Line ~165 in main.py, change:
picosystem.pen(*BLUE)
# to:
picosystem.pen(*RED)
```

**Higher jumps:**
```python
# Line ~14, change:
JUMP_STRENGTH = -10  # was -8
```

**Faster movement:**
```python
# Line ~15, change:
PLAYER_SPEED = 3  # was 2
```

---

## Need Help?

1. Check the full README.md for detailed instructions
2. Try the basic USB drive method first
3. Make sure your file is named exactly `main.py`
4. Restart your Picosystem after uploading

**Ready to code? Start with `main.py` and have fun! 🎮**