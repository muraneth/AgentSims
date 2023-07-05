// SPDX-License-Identifier: MIT
pragma solidity >=0.8.0;
import { System, IWorld } from "solecs/System.sol";
import { getAddressById, addressToEntity } from "solecs/utils.sol";
import { ChatComponent, ID as ChatComponentID, Chat } from "components/ChatComponent.sol";
import { LibMap } from "libraries/LibMap.sol";

uint256 constant ID = uint256(keccak256("system.Chat"));

struct ChatDetail {
    uint256 entityId;
    string detail;
}

contract ChatSystem is System {

  constructor(IWorld _world, address _components) System(_world, _components) {}

  function execute(bytes memory args) public returns (bytes memory) {
    return executeTyped(abi.decode(args, (ChatDetail)));
  }

  function executeTyped(ChatDetail memory chatdetail) public returns (bytes memory) {
    uint256 entityId = addressToEntity(msg.sender);

    Chat memory chat = Chat(chatdetail.detail, chatdetail.entityId);
    ChatComponent chatComponent = ChatComponent(getAddressById(components, ChatComponentID));
    chatComponent.set(entityId, chat);
    return new bytes(0);
  }
}
