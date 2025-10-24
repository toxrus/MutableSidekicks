# MutableSidekicks
An ongoing sample project for the setup of Synty Sidekicks characters in Unreal Engine using Mutable.  
USE FOR TESTING/LEARNING ONLY - THIS IS VERY MUCH WIP, NOT RECOMMENDED FOR USE IN ACTUAL PRODUCTION!  
This project does not include any Sidekicks meshes/assets. They have to be manually added at the correct locations.
Install Instructions:
 - Add Sidekicks to a project in Unity to get access to the fbx asset files.
 - Find the texture file T_ColorMap.png in Assets\Synty\SidekickCharacters\Resources\Textures\, rename it to T_BaseColorMap and drop it into /All/Game/Sidekicks/Base/Textures. The Texture should automatically update the already present texture (this ensures the correct settings for the texture)
 - Find the fbx files in Assets\Synty\SidekickCharacters\Resources\Meshes.
 - Import just the SK_BaseModel.fbx into unreal (Folder: /All/Game/Sidekicks/Base) to check skeletal mesh import settings (In Build: Disable Recompute Normals and Recompute Tangents; set Materials to Import, Do Not Search, Import as Material Instances and for the parent select M_BaseColor, this way when deleting the instances later they can be set to MI_DefaultSidekicks in batch).
 - Drag and drop the Outfits and Species Folders from the unity project (Assets\Synty\SidekickCharacters\Resources\Meshes) into /All/Game/Sidekicks in the unreal project to mass import the skeletal meshes. The meta files will cause warnings since they can't be imported (either ignore or remove .meta before import). Do not use the skeleton of the BaseModel as skeleton target, let the importer create a new skeleton for each mesh. Some skeletons contain "transform" bones that will break the skeleton hierarchy on merge.
 - Depending on which Sidekicks packs are available for you, you might have to remove the datatables references in the composite data tables in /All/Game/Mutable/BodyParts. They are prefixed with CDT_.
 - Files are now ready to use. Open the CO_Sidekick in /All/Game/Mutable and let it compile.
