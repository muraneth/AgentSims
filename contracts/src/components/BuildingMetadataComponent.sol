// SPDX-License-Identifier: MIT
pragma solidity >=0.8.0;
import { BareComponent } from "solecs/BareComponent.sol";
import { LibTypes } from "solecs/LibTypes.sol";

uint256 constant ID = uint256(keccak256("component.BuildingMetadata"));

struct BuildingMetadata {
  string building_name;
  string building_type;
  string room_ids;
}

contract BuildingMetadataComponent is BareComponent {
  constructor(address world) BareComponent(world, ID) {}

  function getSchema() public pure override returns (string[] memory keys, LibTypes.SchemaValue[] memory values) {
    keys = new string[](3);
    values = new LibTypes.SchemaValue[](3);

    keys[0] = "building_name";
    values[0] = LibTypes.SchemaValue.STRING;

    keys[1] = "building_type";
    values[1] = LibTypes.SchemaValue.STRING;

    keys[2] = "room_ids";
    values[2] = LibTypes.SchemaValue.STRING;
  }

  function set(uint256 entity, BuildingMetadata memory buildingMetadata) public {
    set(entity, abi.encode(buildingMetadata.building_name, buildingMetadata.building_type, buildingMetadata.room_ids));
  }

  function getValue(uint256 entity) public view returns (BuildingMetadata memory) {
    (string memory building_name, string memory building_type, string memory room_ids) = abi.decode(getRawValue(entity), (string, string, string));
    return BuildingMetadata(building_name, building_type, room_ids);
  }
}
