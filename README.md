# 💜 ExoticaLX RAT v2.5 💜

<p align="center">
  <img src="https://github.com/deadexotic/exotically-flexing-discord-rat/blob/main/1.jpg?raw=true" width="400">
  <br>
  <em style="color: #9370DB;">Power and stealth in perfect harmony</em>
</p>

<div align="center">
  
[![Python](https://img.shields.io/badge/python-3.8+-8A2BE2?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/github/license/deadexotic/exotically-flexing-discord-rat?style=for-the-badge&color=9370DB)](LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/deadexotic/exotically-flexing-discord-rat?style=for-the-badge&color=800080)](https://github.com/deadexotic/exotically-flexing-discord-rat/commits/main)
  
</div>

<div align="center">
  <h2>✨ Advanced Remote Access Tool with Enhanced Stealth Capabilities ✨</h2>
  <p><strong>⚠️ LEGAL DISCLAIMER: FOR EDUCATIONAL PURPOSES ONLY ⚠️</strong><br>
  <em>Unauthorized use is strictly prohibited and illegal</em></p>
</div>

<hr style="border: 2px solid #9370DB;">

## 🌟 What's New in v2.5

- **🛠️ Enhanced Stability** - Fixed infinite loops and hanging issues across all operations
- **⏱️ Timeout Protection** - Added timeouts to all network operations and long-running processes
- **🧹 Resource Management** - Implemented proper cleanup for threads and processes
- **🔄 Retry Logic** - Added intelligent retry mechanisms with proper limits
- **🛡️ Enhanced AV Evasion** - Improved detection avoidance with dynamic signature masking
- **🔒 Improved Token Security** - Enhanced protection for Discord token handling

## 📋 Command Categories

<table align="center" style="border: 2px solid #9370DB; border-radius: 10px;">
<tr style="background-color: #9370DB;">
  <th style="padding: 10px;">Category</th>
  <th style="padding: 10px;">Commands</th>
</tr>

<tr>
  <td><h3>💻 System Control</h3></td>
  <td>
    <ul>
      <li><code>!shell</code> - Execute command line operations</li>
      <li><code>!remoteshell</code> - Establish reverse shell connection</li>
      <li><code>!uacbypass</code> - Attempt privilege escalation</li>
      <li><code>!sysinfo</code> - Retrieve detailed system information</li>
    </ul>
  </td>
</tr>

<tr style="background-color: rgba(147, 112, 219, 0.1);">
  <td><h3>👁️ Surveillance</h3></td>
  <td>
    <ul>
      <li><code>!webcampic</code> - Capture webcam image</li>
      <li><code>!screenshot</code> - Take screenshot of current display</li>
      <li><code>!windowstart</code> - Begin window activity monitoring</li>
      <li><code>!windowstop</code> - End window monitoring session</li>
    </ul>
  </td>
</tr>

<tr>
  <td><h3>🎮 System Manipulation</h3></td>
  <td>
    <ul>
      <li><code>!voice</code> - Text-to-speech functionality</li>
      <li><code>!wallpaper</code> - Change desktop background</li>
      <li><code>!sing</code> - Play audio in background</li>
      <li><code>!blockinput</code> - Disable user input (requires admin)</li>
    </ul>
  </td>
</tr>

<tr style="background-color: rgba(147, 112, 219, 0.1);">
  <td><h3>📊 Data Acquisition</h3></td>
  <td>
    <ul>
      <li><code>!steal</code> - Extract browser data and credentials</li>
      <li><code>!startkeylogger</code> - Begin keystroke monitoring</li>
      <li><code>!stopkeylogger</code> - End keystroke monitoring</li>
      <li><code>!dumpkeylogger</code> - Retrieve logged keystrokes</li>
      <li><code>!clipboard</code> - Capture clipboard contents</li>
      <li><code>!history</code> - Retrieve browsing history</li>
    </ul>
  </td>
</tr>
</table>

## 🚀 Installation Guide

<div style="background-color: rgba(147, 112, 219, 0.1); padding: 15px; border-radius: 10px; border-left: 4px solid #9370DB;">
  <ol>
    <li>Create a Discord bot and obtain token <a href="https://discordpy.readthedocs.io">here</a></li>
    <li>Add bot to your server with appropriate permissions</li>
    <li>Enable all privileged intents in the Discord Developer Portal</li>
    <li>Run the builder.py script to configure your payload</li>
    <li>Distribute the generated executable to target systems</li>
    <li>Control via Discord commands in your private channel</li>
  </ol>
</div>

## 📚 Full Command List

<details>
<summary style="background-color: #9370DB; color: white; padding: 10px; border-radius: 5px; cursor: pointer;">Click to view all available commands</summary>

<div style="padding: 15px; border: 1px solid #9370DB; border-radius: 0 0 10px 10px;">

### 💻 System Commands

`!shell [command]` - Execute system commands  
`!admincheck` - Verify administrative privileges  
`!sysinfo` - Retrieve system information  
`!cd [directory]` - Change current directory  
`!download [file]` - Download file from target  
`!upload [file]` - Upload file to target

### 👁️ Surveillance

`!webcampic` - Capture webcam image  
`!screenshot` - Capture screen  
`!windowstart` - Begin window activity monitoring  
`!windowstop` - End window monitoring  
`!idletime` - Check user idle time

### 📊 Data Collection

`!steal` - Extract browser data  
`!startkeylogger` - Begin keystroke monitoring  
`!stopkeylogger` - End keystroke monitoring  
`!dumpkeylogger` - Retrieve logged keystrokes  
`!clipboard` - Capture clipboard contents  
`!history` - Retrieve browsing history  
`!geolocate` - Approximate target location

### 🎮 System Control

`!voice [text]` - Text-to-speech output  
`!wallpaper` - Change desktop background  
`!sing [url]` - Play YouTube audio  
`!stopsing` - Stop audio playback  
`!volumemax` - Set volume to maximum  
`!volumezero` - Mute volume  
`!blockinput` - Disable user input (admin required)  
`!unblockinput` - Re-enable user input  
`!write [text]` - Simulate keyboard input  
`!message [text]` - Display message box  
`!exit` - Terminate RAT process  
`!kill [session/all]` - End specific or all sessions

</div>
</details>

## ⚠️ Legal Disclaimer

<div style="background-color: rgba(128, 0, 128, 0.1); padding: 15px; border-radius: 10px; border-left: 4px solid #800080;">
  <p><strong>THIS SOFTWARE IS PROVIDED FOR EDUCATIONAL PURPOSES ONLY.</strong><br>
  UNAUTHORIZED USE IS STRICTLY PROHIBITED AND MAY RESULT IN:</p>
  <ul>
    <li>Criminal prosecution</li>
    <li>Financial penalties</li>
    <li>Law enforcement action</li>
  </ul>
</div>

## 📞 Support

<div align="center" style="margin-top: 20px;">
  <a href="https://t.me/simwiping" style="text-decoration: none; margin: 0 15px;">
    <img src="https://img.shields.io/badge/Telegram-@simwiping-8A2BE2?style=for-the-badge&logo=telegram" alt="Telegram">
  </a>
  <a href="https://discord.com" style="text-decoration: none; margin: 0 15px;">
    <img src="https://img.shields.io/badge/Discord-@hoaofficial-9370DB?style=for-the-badge&logo=discord" alt="Discord">
  </a>
  <a href="https://discord.com" style="text-decoration: none; margin: 0 15px;">
    <img src="https://img.shields.io/badge/Discord-@hqrdcore-9370DB?style=for-the-badge&logo=discord" alt="Discord">
  </a>
</div>
