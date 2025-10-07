# Changelog

All notable changes to the N/U Algebra project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.1.0] - 2025-10-06

### Fixed
- **Critical Installation Bug**: Fixed corrupted text in `setup.py` that caused CI/CD failures and prevented package installation
  - Removed invalid "ic.```python" prefix from line 1 of setup.py
  - Package now installs correctly via `pip install -e .`
  - Resolved "Getting requirements to build editable" error (exit code 1)

### Added
- **Comprehensive Test Suite**: Added 467 tests in `test_nu_algebra.py` covering core operations
- **Validation Tests**: Added 438 validation tests in `test_validation.py` for numerical accuracy
- **Python Examples**:
  - Basic operations demonstration (`basic_operations.py`)
  - Engineering application example (`engineering_example.py`)
  - Psychology/social science example (`psychology_example.py`)
- **R Examples**: Complete R implementation examples (`basic_operations.R`)
- **Documentation Structure**:
  - Integration guides framework (`docs/integration_guides.md`)
  - Theoretical foundation documentation (`docs/theoretical_foundation.md`)
  - Validation results documentation (`docs/validation_results.md`)
- **GitHub Actions CI/CD**: Automated testing workflow (`main.yml`)
- **Data Management**: Data directory structure with README (`data/README.md`)
- **Project Infrastructure**:
  - Standard Python package structure with `src/` directory
  - Requirements specification (`requirements.txt`)
  - Package metadata (`CITATION.cff`)
  - Enhanced `.gitignore` for Python projects

### Changed
- **README Enhancement**: Significantly expanded with detailed usage examples, validation results, and citation information
- **Code Organization**: Migrated core implementations to `src/` directory:
  - `src/nu_algebra.py` (395 lines of enhanced Python implementation)
  - `src/nu_algebra.R` (347 lines of R implementation)
- **License Update**: Clarified CC BY 4.0 license terms
- **CI/CD Workflow**: Replaced old `ci.yml` with improved `main.yml`

### Removed
- **Large Binary Files**: Removed 6.9MB validation dataset ZIP from repository (available via Zenodo DOI instead)
- **Root-level Implementation Files**: Moved `nu_algebra.py` and `nu_algebra.R` to `src/` directory

## [v.73] - 2025-01-01

### Added
- Initial public release
- Core N/U Algebra implementation
- Basic documentation

---

## Version Numbering

Starting with v3.1.0, this project follows semantic versioning:
- **MAJOR** version: Incompatible API changes
- **MINOR** version: Backwards-compatible functionality additions
- **PATCH** version: Backwards-compatible bug fixes

## Links
- [Zenodo Dataset DOI](https://doi.org/10.5281/zenodo.17221863)
- [Project Documentation](https://doi.org/10.5281/zenodo.17172694)
- [GitHub Repository](https://github.com/abba-01/nualgebra)
