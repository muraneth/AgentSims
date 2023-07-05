// SPDX-License-Identifier: MIT
pragma solidity >=0.8.0;
import { IWorld } from "solecs/interfaces/IWorld.sol";
import { EquipmentTypeComponent, ID as EquipmentTypeComponentID, EquipmentType } from "components/EquipmentTypeComponent.sol";

import { LibEquipmentProperties } from "./LibEquipmentProperties.sol";

library EquipmentTypeInitializer {


  function init1(IWorld world) internal {
    EquipmentTypeComponent equipmentType = EquipmentTypeComponent(world.getComponent(EquipmentTypeComponentID));

    LibEquipmentProperties.EquipmentProperties[] memory equipments = LibEquipmentProperties.getAllObjectTypes1();
    uint256 size = equipments.length;

    for (uint256 i = 0; i < size; i++) {
      uint256 entity = world.getUniqueEntityId();

      LibEquipmentProperties.EquipmentProperties memory obj = equipments[i];
      equipmentType.set(entity, EquipmentType(obj.name, obj.description, obj.operations));
    }
  }

  function init2(IWorld world) internal {
    EquipmentTypeComponent equipmentType = EquipmentTypeComponent(world.getComponent(EquipmentTypeComponentID));

    LibEquipmentProperties.EquipmentProperties[] memory equipments = LibEquipmentProperties.getAllObjectTypes2();
    uint256 size = equipments.length;

    for (uint256 i = 0; i < size; i++) {
      uint256 entity = world.getUniqueEntityId();

      LibEquipmentProperties.EquipmentProperties memory obj = equipments[i];
      equipmentType.set(entity, EquipmentType(obj.name, obj.description, obj.operations));
    }
  }


  // Init EquipmentProperties
  function init(IWorld world) internal {
    init1(world);
    init2(world);
  }

}
