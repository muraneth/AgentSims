// SPDX-License-Identifier: MIT
pragma solidity >=0.8.0;
import { BareComponent } from "solecs/BareComponent.sol";
import { LibTypes } from "solecs/LibTypes.sol";

uint256 constant ID = uint256(keccak256("component.Transform"));

struct Transform {
  int32 position_x;
  int32 position_y;
  uint16 rotation;
}

contract TransformComponent is BareComponent {
  constructor(address world) BareComponent(world, ID) {}

  function getSchema() public pure override returns (string[] memory keys, LibTypes.SchemaValue[] memory values) {
    keys = new string[](3);
    values = new LibTypes.SchemaValue[](3);

    keys[0] = "position_x";
    values[0] = LibTypes.SchemaValue.INT32;

    keys[1] = "position_y";
    values[1] = LibTypes.SchemaValue.INT32;

    keys[2] = "rotation";
    values[2] = LibTypes.SchemaValue.UINT16;
  }

  function set(uint256 entity, Transform memory transform) public {
    set(entity, abi.encode(transform.position_x, transform.position_y, transform.rotation));
  }

  function getValue(uint256 entity) public view returns (Transform memory) {
    (int32 position_x, int32 position_y, uint16 rotation) = abi.decode(getRawValue(entity), (int32, int32, uint16));
    return Transform(position_x, position_y, rotation);
  }
}
