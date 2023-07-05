// SPDX-License-Identifier: MIT
pragma solidity >=0.8.0;
import { StringComponent } from "std-contracts/components/StringComponent.sol";
// import { LibTypes } from "solecs/LibTypes.sol";

uint256 constant ID = uint256(keccak256("component.Animation"));

// struct Animation {
//   string animation_state;
//   uint64 updated_at;
// }

contract AnimationComponent is StringComponent {
  constructor(address world) StringComponent(world, ID) {}

  // function getSchema() public pure override returns (string[] memory keys, LibTypes.SchemaValue[] memory values) {
  //   keys = new string[](2);
  //   values = new LibTypes.SchemaValue[](2);

  //   keys[0] = "animation_state";
  //   values[0] = LibTypes.SchemaValue.STRING;

  //   keys[1] = "updated_at";
  //   values[1] = LibTypes.SchemaValue.UINT64;
  // }

  // function set(uint256 entity, Animation memory animation) public {
  //   set(entity, abi.encode(animation.animation_state, animation.updated_at));
  // }

  // function getValue(uint256 entity) public view returns (Animation memory) {
  //   (string memory animation_state, uint64 updated_at) = abi.decode(getRawValue(entity), (string, uint64));
  //   return Animation(animation_state, updated_at);
  // }
}
