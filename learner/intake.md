# Mentor notes (intake)

Written by the mentor who set this repo up. Onboarding confirms it with the learner instead of asking everything again. Context only: what they actually know is measured from their answers.

## Who
A medical student.

## Goal
To work with neuroimaging data (MRI/fMRI) in a research lab, using Python and **nilearn** (https://nilearn.github.io/stable/index.html): load and explore data, visualize brain maps, read and adapt existing analysis scripts and notebooks, and interpret the results correctly.

## What matters most
AI tools will write part of the code. So the priority is being able to **read, run, verify and debug** code, and to understand the data and the analysis steps well enough to notice when something is wrong. Rote syntax and software-engineering depth (classes, decorators, web, packaging) are out of scope unless the goal needs them.

## Starting point
No programming experience. Don't treat medical knowledge as programming knowledge. In the neuroimaging part, anatomy and clinical knowledge can be a real bridge, so use it there.

## Time
About 30–60 minutes a day.

## Planned path (a proposal: new-track refines it with research; confirm with the learner)
1. `python-foundations`: Python from zero, cut to what the goal needs (values, variables, types, conditions, loops, lists and dicts, functions, imports, files and paths, reading errors).
2. `scientific-python`: NumPy arrays (shape, indexing, 3D/4D thinking), tables with pandas (e.g. events and confounds files), matplotlib, Jupyter notebooks.
3. `nilearn`: neuroimaging concepts just in time (NIfTI, voxel, affine, 4D images, BIDS), then loading, plotting, maskers and a first simple analysis.

During track 1, show now and then where the current concept appears in nilearn work, so the goal stays visible.

## Language
Turkish, with standard English technical terms in parentheses (değişken (variable), fonksiyon (function), array, dataframe, voxel …).
