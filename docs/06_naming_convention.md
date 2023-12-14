# Naming Convention

Cheching namin convention is a generic rule. These rules are needed to run on all kinds of assets. Either it is a 3D model, a texture, a sound, etc. The rules are the same for all assets.
Directories are not considered as assets but it is easy to define rules for them too.

To design a generic rule for checking the naming convention of assets in QuVery, we have to consider the following points:

- The name of the asset should be unique.
- The name of the asset should be descriptive.
- The name of the asset should be consistent.

### Unique

This means that the name of the asset should be unique in the project. This is important because it will be used to identify the asset in the project.

### Descriptive

The name of the asset should be able to describe the asset. By reading the name of the asset, we should be able to know what the asset is about and what it is used for.

### Consistent

The name of the asset should be consistent with the other assets in the project. This means that the name of the asset should follow the same naming convention as the other assets in the project. It will make it easier to find the asset in the project.

## Some Naming Convention Examples
### UE5 Naming Convention

[Recommended Asset Naming Convention in UE5](https://docs.unrealengine.com/5.3/en-US/recommended-asset-naming-conventions-in-unreal-engine-projects/)
[UE5 Style](https://github.com/Allar/ue5-style-guide)

[AssetTypePrefix]_[AssetName]_[Descriptor]_[OptionalVariantLetterOrNumber]

Eample: 
- A static mesh for a table in the game would be named SM_Table_Wood_01
- A diffuse/albedo/color texture for a table in the game would be named T_Table_Wood_01_D
- If we have multiple versions of the metal door with different diffuse textures, we would name those T_Door_Metal_01_D, T_Door_Metal_02_D, etc.
- A no

### Unity Naming Convention by Justin Wasilenko

[Unity Asset Naming Conventions](https://github.com/justinwasilenko/Unity-Style-Guide?tab=readme-ov-file#4-asset-naming-conventions)

[AssetTypePrefix]_[AssetName]_[Variant]_[Suffix]

Example:
- A static mesh for a table in the game would be named SM_Table_Wood_01

