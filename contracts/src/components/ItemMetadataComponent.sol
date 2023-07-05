// SPDX-License-Identifier: MIT
pragma solidity >=0.8.0;
import "solecs/Component.sol";

uint256 constant ID = uint256(keccak256("component.ItemMetadata"));

struct ItemMetadata {
  string item_name;
  string item_type;
  string item_function;
}

contract ItemMetadataComponent is Component {
  constructor(address world) Component(world, ID) {}

  function getSchema() public pure override returns (string[] memory keys, LibTypes.SchemaValue[] memory values) {
    keys = new string[](3);
    values = new LibTypes.SchemaValue[](3);

    keys[0] = "item_name";
    values[0] = LibTypes.SchemaValue.STRING;

    keys[1] = "item_type";
    values[1] = LibTypes.SchemaValue.STRING;

    keys[2] = "item_function";
    values[2] = LibTypes.SchemaValue.STRING;
  }

  function set(uint256 entity, ItemMetadata calldata value) public virtual {
    set(entity, abi.encode(value.item_name, value.item_type, value.item_function));
  }

  function getValue(uint256 entity) public view virtual returns (ItemMetadata memory) {
    (string memory item_name, string memory item_type, string memory item_function) = abi.decode(getRawValue(entity), (string, string, string));
    return ItemMetadata(item_name, item_type, item_function);
  }

  function getEntitiesWithValue(ItemMetadata calldata value) public view virtual returns (uint256[] memory) {
    return getEntitiesWithValue(abi.encode(value));
  }
}