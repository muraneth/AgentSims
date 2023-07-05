// SPDX-License-Identifier: MIT
pragma solidity >=0.8.0;
import { StringComponent } from "std-contracts/components/StringComponent.sol";

uint256 constant ID = uint256(keccak256("component.Status"));

contract StatusComponent is StringComponent {
  constructor(address world) StringComponent(world, ID) {}

  // function getSchema() public pure override returns (string[] memory keys, LibTypes.SchemaValue[] memory values) {
  //   keys = new string[](2);
  //   values = new LibTypes.SchemaValue[](2);

  //   keys[0] = "status";
  //   values[0] = LibTypes.SchemaValue.STRING;

  //   keys[1] = "updated_at";
  //   values[1] = LibTypes.SchemaValue.UINT64;
  // }

  // function set(uint256 entity, Status memory status) public {
  //   set(entity, abi.encode(status.status, status.updated_at));
  // }

  // function getValue(uint256 entity) public view returns (Status memory) {
  //   (string memory status, uint64 updated_at) = abi.decode(getRawValue(entity), (string, uint64));
  //   return Status(status, updated_at);
  // }
}
