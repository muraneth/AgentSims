// SPDX-License-Identifier: MIT
pragma solidity >=0.8.0;
import { BareComponent } from "solecs/BareComponent.sol";
import { LibTypes } from "solecs/LibTypes.sol";

uint256 constant ID = uint256(keccak256("component.Chat"));

struct Chat {
  string chat_detail;
  uint256 target_id;
}

contract ChatComponent is BareComponent {
  constructor(address world) BareComponent(world, ID) {}

  function getSchema() public pure override returns (string[] memory keys, LibTypes.SchemaValue[] memory values) {
    keys = new string[](2);
    values = new LibTypes.SchemaValue[](2);

    keys[0] = "chat_detail";
    values[0] = LibTypes.SchemaValue.STRING;

    keys[1] = "target_id";
    values[1] = LibTypes.SchemaValue.UINT256;
  }

  function set(uint256 entity, Chat memory chat) public {
    set(entity, abi.encode(chat.chat_detail, chat.target_id));
  }

  function getValue(uint256 entity) public view returns (Chat memory) {
    (string memory chat_detail, uint256 target_id) = abi.decode(getRawValue(entity), (string, uint256));
    return Chat(chat_detail, target_id);
  }
}
