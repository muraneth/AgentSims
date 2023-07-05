// SPDX-License-Identifier: MIT
pragma solidity >=0.8.0;
import "solecs/Component.sol";

uint256 constant ID = uint256(keccak256("component.Equipment"));

struct EquipmentType {
  string name;
  string description;
  string[] operations;
}

contract EquipmentTypeComponent is Component {
  constructor(address world) Component(world, ID) {}

  function getSchema() public pure override returns (string[] memory keys, LibTypes.SchemaValue[] memory values) {
    keys = new string[](3);
    values = new LibTypes.SchemaValue[](3);

    keys[0] = "name";
    values[0] = LibTypes.SchemaValue.STRING;

    keys[1] = "description";
    values[1] = LibTypes.SchemaValue.STRING;

    keys[2] = "operations";
    values[2] = LibTypes.SchemaValue.STRING_ARRAY;
  }

  function set(uint256 entity, EquipmentType calldata value) public virtual {
    set(entity, abi.encode(value.name, value.description, value.operations));
  }

  function getValue(uint256 entity) public view virtual returns (EquipmentType memory) {
    (string memory name, string memory description, string[] memory operations) = abi.decode(getRawValue(entity), (string, string, string[]));
    return EquipmentType(name, description, operations);
  }

  function getEntitiesWithValue(EquipmentType calldata coord) public view virtual returns (uint256[] memory) {
    return getEntitiesWithValue(abi.encode(coord));
  }
}