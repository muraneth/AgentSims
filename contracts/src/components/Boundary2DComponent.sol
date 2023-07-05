// SPDX-License-Identifier: MIT
pragma solidity >=0.8.0;
import "solecs/Component.sol";

uint256 constant ID = uint256(keccak256("component.Boundary2D"));

struct Boundary2D {
  int32 topLeftX;
  int32 topLeftY;
  int32 bottomRightX;
  int32 bottomRightY;
}

contract Boundary2DComponent is Component {
  constructor(address world) Component(world, ID) {}

  function getSchema() public pure override returns (string[] memory keys, LibTypes.SchemaValue[] memory values) {
    keys = new string[](4);
    values = new LibTypes.SchemaValue[](4);

    keys[0] = "topLeftX";
    values[0] = LibTypes.SchemaValue.INT32;

    keys[1] = "topLeftY";
    values[1] = LibTypes.SchemaValue.INT32;

    keys[2] = "bottomRightX";
    values[2] = LibTypes.SchemaValue.INT32;

    keys[3] = "bottomRightY";
    values[3] = LibTypes.SchemaValue.INT32;
  }

  function set(uint256 entity, Boundary2D calldata value) public virtual {
    set(entity, abi.encode(value));
  }

  function getValue(uint256 entity) public view virtual returns (Boundary2D memory) {
    (int32 topLeftX, int32 topLeftY, int32 bottomRightX, int32 bottomRightY) = abi.decode(getRawValue(entity), (int32, int32, int32, int32));
    return Boundary2D(topLeftX, topLeftY, bottomRightX, bottomRightY);
  }

  function getEntitiesWithValue(Boundary2D calldata coord) public view virtual returns (uint256[] memory) {
    return getEntitiesWithValue(abi.encode(coord));
  }
}
