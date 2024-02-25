# gen3-pokemon-audio-adjust
A tool to adjust the audio files for gen3 pokemon decompilations to sound correct when emulated in fast forward.

## Requirements

* Python, recommended version >= 3.7
* [pydub](https://pypi.org/project/pydub/) libary
* A compatible gen-3 pokemon decompilation:
  * [**Pokémon Ruby and Sapphire**](https://github.com/pret/pokeruby)
  * [**Pokémon FireRed and LeafGreen**](https://github.com/pret/pokefirered)
  * [**Pokémon Emerald**](https://github.com/DizzyEggg/pokeemerald)
  * [**Pokémon Emerald Expansion**](https://github.com/rh-hideout/pokeemerald-expansion)
## Usage

Simply point `config.json` at the \sound directory for your pokemon decompilation and run adjust_audio.py. This will modify all .aif sound samples and .s songs. Also produced are backup files, although it's reccomended to manage your decomp with git and not solely rely on the backups.

The decompilation can be restored to it's origional state using restore_backup.py

By default `speed_factor` is 0.5, meaning all sounds are slowed down by half and will sound normal when an emulator is ran at *2 speed. A factor of 0.25 would be appropriate for a *4 speed emulation, however, in practice the effect doesn't work so well for speeds beyond *2 - adjust at your own peril!
