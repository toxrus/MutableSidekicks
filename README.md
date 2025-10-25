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


How to use the asset action utility to "fix" the transform bones issue:
- Set the python path to include the supplied .py file. In project settings filter for python, under additional path select the ... and browse to the python folder inside the project at \Content\AssetActionUtils\Python. Confirm with Select Folder.
- Restart the project
- Right clicking any skeletal mesh now provides a new option "Scripted Asset Actions". The only option available is "Fix Sidekicks Skeleton"
- Running the command will reparent the bones and remove the transform bones when found. This will cause a popup to appear about not being able to merge the skeleton.
- Select new skeleton in the prompt, overwrite the old skeleton. All references are fixed up automatically
- Doing this across ALL sidekicks assets at once can get quite laggy due to Editor info window popups. I recommend doing one pack at a time.
- Once all assets have been processed this way, no warnings should appear in the CO_Sidekicks on compile warning about not being able to merge skeletons.
