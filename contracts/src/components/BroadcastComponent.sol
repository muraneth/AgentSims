// SPDX-License-Identifier: MIT
pragma solidity >=0.8.0;
import { StringComponent } from "std-contracts/components/StringComponent.sol";

uint256 constant ID = uint256(keccak256("component.Broadcast"));

// struct Broadcast {
//   string plan;
//   uint64 updated_at;
// }

contract BroadcastComponent is StringComponent {
  constructor(address world) StringComponent(world, ID) {}

  // function getSchema() public pure override returns (string[] memory keys, LibTypes.SchemaValue[] memory values) {
  //   keys = new string[](2);
  //   values = new LibTypes.SchemaValue[](2);

  //   keys[0] = "plan";
  //   values[0] = LibTypes.SchemaValue.STRING;

  //   keys[1] = "updated_at";
  //   values[1] = LibTypes.SchemaValue.UINT64;
  // }

  // function set(uint256 entity, Plan memory plan) public {
  //   set(entity, abi.encode(plan.plan, plan.updated_at));
  // }

  // function getValue(uint256 entity) public view returns (Plan memory) {
  //   (string memory plan, uint64 updated_at) = abi.decode(getRawValue(entity), (string, uint64));
  //   return Plan(plan, updated_at);
  // }
}
