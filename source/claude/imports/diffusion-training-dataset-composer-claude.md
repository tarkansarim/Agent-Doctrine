# Imported Claude Doctrine Source

- Source path: `<workspace root>/Diffusion_Training_Dataset_Composer/CLAUDE.md`
- Source SHA256: `66b33f4788158bb53468cb85bda161d63fb17ea88486f01240775b1852dc0842`
- Provider lane: `claude`

## Original Content

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with this repository.

## Project Overview

Diffusion Training Dataset Composer is a PyQt5-based GUI tool for creating training datasets for diffusion models (Stable Diffusion, Flux, etc.). It supports both LoRA/DreamBooth (character/subject training) and Fine-tuning (style/concept training) workflows.

## Quick Start

### Setup & Running
```bash
# Windows
windows_install.bat  # Creates venv and installs dependencies
windows_run_app.bat  # Runs the application

# Linux
./linux_install.sh   # Creates venv and installs dependencies
./linux_run.sh       # Runs the application
```

### Development Tips
- Press `Ctrl+R` to refresh directory listings
- Check `sampler.log` in destination folders for debugging
- Save/Load configurations via File menu

## Architecture Overview

Single-file application: `image_sampler_tool.py`

### Main Components

1. **MainWindow** - Three-column layout:
   - Left: Settings and execution controls
   - Middle: Source folder management  
   - Right: Regularization folder controls

2. **FolderWidget** - Individual folder controls:
   - Image count selection with megapixel awareness
   - Caption distribution (blank/basic/detailed/structured)
   - Kohya SS configuration (instance/class prompts, repeats)

3. **Worker Thread** - Background processing:
   - Concurrent image copying/conversion
   - Megapixel-aware sampling
   - Progress reporting

4. **TrainingStrategyPanel** - Bottom panel:
   - Training calculations (steps, learning rate)
   - Phase-specific recommendations

### Key Features

#### Dynamic Regularization Sliders
- **Equilibrium System**: Sliders maintain constant total weight
- **Bidirectional Movement**: Moving slider right steals points, left returns them
- **Predetermined Pattern**: Each drag session uses fixed random order
- **Reversible Operations**: Same sliders affected when moving back and forth

#### Megapixel-Aware Sampling
- Balances dataset by image resolution
- Prevents bias toward high/low resolution images
- Real-time megapixel calculations and indicators

#### Caption Distribution System
- Four caption types with percentage controls
- Automatic validation (must sum to 100%)
- Mode-specific behavior (LoRA excludes blank captions)

## Implementation Details

### State Management
- **QSettings**: Persistent user preferences
- **Equilibrium Tracking**: `reg_slider_equilibrium` maintains slider totals
- **Redistribution Order**: Generated per drag session for consistent behavior

### Threading Model
- **Main Thread**: UI updates only
- **Worker QThread**: Image processing coordination
- **ThreadPoolExecutor**: Concurrent file operations
- **ProcessPoolExecutor**: PNG conversions

### Visual Design
- **Color Coding**: Green (valid), Red (error), Orange (warning)
- **24 Pastel Colors**: Folder differentiation
- **Responsive Layout**: 35% screen width, 85% height

## Common Tasks

### Adding New Features
1. Check existing patterns in the codebase
2. Use Qt signals/slots for event handling
3. Maintain thread safety (UI updates in main thread only)
4. Add tooltips for user guidance

### Modifying Slider Behavior
- See `redistribute_slider_weights()` for equilibrium logic
- Check `on_slider_pressed()` for redistribution setup
- Update `on_slider_move()` for drag behavior

### Working with Captions
- Caption types in `CAPTION_TYPES` constant
- Distribution stored in `FolderEntry.caption_distribution`
- File matching supports `.txt` and `.caption` extensions

## Key Data Structures

```python
@dataclass
class FolderEntry:
    path: str
    image_count: int = 100
    blank: int = 5
    basic: int = 15  
    detailed: int = 30
    structured: int = 50
    instance_prompt: str = ""
    class_prompt: str = "a person"
    repeats: int = 1
    caption_distribution: dict = None
```

## Constants
- **IMAGE_EXTENSIONS**: `{".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif", ".gif"}`
- **DEFAULT_RESIZE**: 1024 pixels (shortest side)
- **THREAD_POOL_SIZE**: 8 workers for file operations
- **PROCESS_POOL_SIZE**: 4 workers for PNG conversion
