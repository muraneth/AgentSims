// SPDX-License-Identifier: MIT
pragma solidity >=0.8.0;

library LibAreas {
    struct AreaInfo {
        string name;
        int32 x;
        int32 y;
        int32 width;
        int32 height;
    }

    function getAreas() internal pure returns (AreaInfo[] memory) {
        AreaInfo[] memory areas = new AreaInfo[](6);
        areas[0] = AreaInfo("Church", 4, 48, 14, 9);
        areas[1] = AreaInfo("Workshop", 4, 29, 25, 15);
        areas[2] = AreaInfo("Temple", 55, 28, 37, 14);
        areas[3] = AreaInfo("Workshop", 119, 29, 25, 15);
        areas[4] = AreaInfo("Station", 125, 50, 19, 20);
        areas[5] = AreaInfo("Plaza", 56, 55, 35, 21);
        return areas;
    }
}