// SPDX-License-Identifier: MIT
pragma solidity >=0.8.0;
import { BareComponent } from "solecs/BareComponent.sol";
import { LibTypes } from "solecs/LibTypes.sol";
import { SingletonID } from "solecs/SingletonID.sol";

uint256 constant ID = uint256(keccak256("component.Card"));

enum SUIT {
    Clubs,
    Diamonds,
    Hearts,
    Spades
}

enum RANK {
    Ace,
    Two,
    Three,
    Four,
    Five,
    Six,
    Seven,
    Eight,
    Nine,
    Ten,
    Jack,
    Queen,
    King
}

struct Card {
  SUIT suit;
  RANK rank;
}

// struct Cards {
//     Card[] cards;
// }

contract CardComponent is BareComponent {
  constructor(address world) BareComponent(world, ID) {}

  function getSchema() public pure override returns (string[] memory keys, LibTypes.SchemaValue[] memory values) {
    keys = new string[](2);
    values = new LibTypes.SchemaValue[](2);

    keys[0] = "suit";
    values[0] = LibTypes.SchemaValue.UINT32;

    keys[1] = "rank";
    values[1] = LibTypes.SchemaValue.UINT32;
  }

  function set(uint256 entity, Card calldata value) public virtual {
    set(entity, abi.encode(value));
  }

  function getValue(uint256 entity) public view virtual returns (Card memory) {
    (SUIT suit, RANK rank) = abi.decode(getRawValue(entity), (SUIT, RANK));
    return Card(suit, rank);
  }
}
