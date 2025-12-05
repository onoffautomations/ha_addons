# Changelog

All notable changes to the HA Network Scanner project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2025-12-05

### Added
- **System Theme Preference**: Theme now defaults to system preference (auto mode) but can be manually overridden
  - Three theme modes: Auto (follows system), Light, and Dark
  - Theme toggle button cycles through: Auto → Light → Dark → Auto
  - Automatically responds to system theme changes when in Auto mode
  - Theme preference is saved to localStorage
  - Updated button tooltips to indicate current theme mode

### Changed
- **Mobile UI Improvements**: Complete responsive design overhaul for better mobile experience
  - Optimized layout for tablets (≤768px) and mobile phones (≤480px)
  - Controls now stack better on smaller screens with improved spacing
  - Search box and auto-refresh toggle reorder for better mobile UX
  - Stats cards adapt to single column on very small screens
  - Table is now horizontally scrollable on mobile with smooth touch scrolling
  - Subnet configuration panels stack vertically on mobile
  - Modal dialogs are now 95% width/height on mobile for better space utilization
  - Improved touch targets (44x44px minimum) on touch devices for better accessibility
  - Reduced font sizes and padding appropriately for smaller screens
  - Protocol selection buttons stack vertically on mobile
  - Better landscape orientation support for modals

### Fixed
- **Mobile Button Layout**: Fixed critical mobile UI issues
  - Scan Network button now properly displays full width on mobile devices
  - Auto-refresh toggle now has proper styling with background panel on mobile
  - Theme toggle button properly sized with correct padding on mobile
  - Secondary action buttons (Refresh, Export JSON, Export CSV) now flex properly
  - Improved button ordering and layout with CSS order properties

### Improved
- Theme system architecture for better maintainability
- Touch interaction on mobile devices with larger, more accessible tap targets
- Modal visibility and usability on small screens
- Button layout and wrapping on narrow viewports
- Overall mobile user experience and interface consistency
