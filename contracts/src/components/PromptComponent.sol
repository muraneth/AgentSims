// SPDX-License-Identifier: MIT
pragma solidity >=0.8.0;
import { BareComponent } from "solecs/BareComponent.sol";
import { LibTypes } from "solecs/LibTypes.sol";

uint256 constant ID = uint256(keccak256("component.Prompt"));

struct Prompt {
  string prompt_detail;
  uint256 source_id;
}

contract PromptComponent is BareComponent {
  constructor(address world) BareComponent(world, ID) {}

  function getSchema() public pure override returns (string[] memory keys, LibTypes.SchemaValue[] memory values) {
    keys = new string[](2);
    values = new LibTypes.SchemaValue[](2);

    keys[0] = "prompt_detail";
    values[0] = LibTypes.SchemaValue.STRING;

    keys[1] = "source_id";
    values[1] = LibTypes.SchemaValue.UINT256;
  }

  function set(uint256 entity, Prompt memory chat) public {
    set(entity, abi.encode(chat.prompt_detail, chat.source_id));
  }

  function getValue(uint256 entity) public view returns (Prompt memory) {
    (string memory prompt_detail, uint256 source_id) = abi.decode(getRawValue(entity), (string, uint256));
    return Prompt(prompt_detail, source_id);
  }
}
