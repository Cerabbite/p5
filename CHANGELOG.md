# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Calendar Versioning](https://calver.org/).

## 2024.4.2 (UNRELEASED)

### Added:
- `reinstate` command that adds all p5js files back in
- `clear` command that clears a project of all p5js files
- The `create` command now also creates a `p5.toml` config file

### Changed:
- When the `create` command fails it deletes the created folder automatically
- `create` command now asks you if you want to continue if project folder already exists

## 2024.4.1

### Fixed:
- Console prints `vLATEST` instead of `v{version number}` when creating a project with the latest version of p5js

## 2024.4.0

### Added:
- Upgrade command
- Ability to upgrade/downgrade to any version of p5js you chose

## 2024.4.0a1

### Added:
- Create command
- Ability to chose any version of p5js when creating project
