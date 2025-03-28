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

  Mostly, Pygame-ce was heavily dependent on the CPU, which limits graphical possibilities. Arcade here is leveraging the GPU resources. 
  
  It also includes **built-in tools** for:
  - animations, 
  - sprite management, 
  - scene transitions, 
  - and hardware-accelerated rendering,   
  
  making it easier and faster to build polished 2D games without writing everything from scratch.

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
