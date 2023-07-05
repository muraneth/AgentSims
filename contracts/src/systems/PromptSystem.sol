// SPDX-License-Identifier: MIT
pragma solidity >=0.8.0;
import { System, IWorld } from "solecs/System.sol";
import { getAddressById, addressToEntity } from "solecs/utils.sol";
import { PromptComponent, ID as PromptComponentID, Prompt } from "components/PromptComponent.sol";
import { LibMap } from "libraries/LibMap.sol";

uint256 constant ID = uint256(keccak256("system.Prompt"));

struct PromptDetail {
    uint256 targetId;
    string detail;
}

contract PromptSystem is System {

  constructor(IWorld _world, address _components) System(_world, _components) {}

  function execute(bytes memory args) public returns (bytes memory) {
    return executeTyped(abi.decode(args, (PromptDetail)));
  }

  function executeTyped(PromptDetail memory promptdetail) public returns (bytes memory) {
    // uint256 entityId = addressToEntity(msg.sender);

    // TODO: can only send prompt to owner's agent
    // TODO: time limit
    Prompt memory prompt = Prompt(promptdetail.detail, promptdetail.targetId);
    PromptComponent(getAddressById(components, PromptComponentID)).set(promptdetail.targetId, prompt);
    return new bytes(0);
  }
}
