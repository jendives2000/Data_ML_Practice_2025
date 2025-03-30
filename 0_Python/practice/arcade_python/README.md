# **Hands-On Python 🐍: Platformer Game 🧱 using Arcade 3 🎮**

---

By Jean-Yves Tran | jy.tran@[datascience-jy.com](https://datascience-jy.com) | [LinkedIn](https://www.linkedin.com/in/jytran-datascience/)  
IBM Certified Data Analyst 

---
![alt text](jeanyves-tran_python_arcadeV3_gameDev_2025-03-28-1.gif)
---

Source: 
- [Simple Platformer](https://api.arcade.academy/en/latest/tutorials/platform_tutorial/index.html) - api.arcade.academy |  Paul Vincent Craven
- [Arcade Docs](https://api.arcade.academy/en/latest/index.html) - Arcade Official Documentation
---

- **WHY ARCADE?**  
  Using the **Arcade** library over **Pygame-ce** offers clear advantages for learners who want to deepen their understanding of Python and write cleaner, more maintainable code. 
  
  Arcade is fully object-oriented, making it ideal for practicing real-world programming structures like class inheritance, modular architecture, and event-based logic — all of which translate well to data analysis and machine learning workflows. 

- **Pygame Vs Arcade**:
  
  Mostly, Pygame-ce offers full-customization on any aspect of the game, this comes at some costs: more boiler-plate and more verbosity, which require more testings and monitoring of the code. 
  
  Pygame-ce is heavily dependent on the CPU, which limits graphical possibilities. Arcade here is leveraging the GPU resources. 
  
  It also includes **built-in tools** for:
  - animations, 
  - sprite management, 
  - scene transitions, 
  - and hardware-accelerated rendering,   
  
  making it easier and faster to build polished 2D games without writing everything from scratch.  

  **Other Main Differences**: 
  - **Unified Game Loop via Subclassing arcade.Window**  
    Arcade centralizes the game loop and input management using an OOP pattern by subclassing arcade.Window (or arcade.View), which encapsulates on_draw, on_update, and input methods like on_key_press.

        >> class GameView(arcade.Window):  
              def on_draw(self): ...  
              def on_update(self, delta_time): ...  
    
    - Why it’s better:  
  
      In Pygame, the main loop is procedural and scattered. You manage everything manually (while running:), making it harder to modularize or swap game states.

    ➡️ Better separation of concerns and cleaner extensibility in Arcade.

  - **Built-in Scene Graph (arcade.Scene):**  
    Arcade introduces arcade.Scene, which organizes sprite layers (Player, Coins, Platforms, Foreground, etc.).

        >> self.scene = arcade.Scene.from_tilemap(self.tile_map)
           self.scene.add_sprite("Player", self.player_sprite)
    
    - Why it’s better:  
    In Pygame, you manage multiple pygame.sprite.Group() objects manually and have to handle draw order explicitly.

    ➡️ Scene abstraction reduces boilerplate, enforces better layer structure, and scales more easily.

  - **Asset Loading with Virtual Paths**  
    Arcade supports resource aliasing (e.g., :resources:images/...) that makes asset loading easier and platform-independent.

        >> arcade.load_texture(":resources:images/...")
           arcade.load_tilemap(":resources:tiled_maps/...")
    
    - **Why it’s better**:  
    In Pygame, asset management often requires fragile manual path hacks (os.path.join, sys.path.append, etc.) — especially hard when packaging with PyInstaller.

    ➡️ Arcade's asset paths are clean, relocatable, and don't require custom path utilities.
  
  - and several other improvements: 
    - Tilemap Integration with Tiled
    - Physics Engine Abstraction
    - GUI Layer Separation (Camera2D)
    - Built-in Audio with Clean Syntax

Like the previous Pygame-ce project, this one is also a practice project where I:
- put to use 
- enhance my **Python skills**
- and my **game development skills**,  
to develop a simple platformer game in Arcade version 3.  

I followed an official written tutorial from Arcade. 
The graphical assets were all included in the library itself. 

**NOT WSL2 COMPLIANT ON WIN 10**:  
If you are using a virtual linux environment on Windows 10 (not 11) thanks to WSL2 be aware that this code WILL NOT behave as expected due to limitations:  
- no music
- no level advancement (from level 1 to level 2): the game will simply crash

Otherwise, just make sure that:
- you do not use a Linux environment
- on a Windows 10 OS
- OR you run this code out of the WSL2 linux environment, so straight from your Windows OS
- or you do run it from WSL2 (actually WSLg) Linux on a WIN 11
