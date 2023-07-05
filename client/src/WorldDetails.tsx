import { useState, useEffect } from 'react';
import {
  EntityIndex
} from "@latticexyz/recs";
import { useComponentValue } from "@latticexyz/react";
import { useMUD } from "./MUDContext";
import { World } from "./world/World";
import { config } from "./mud/config";

import styles from './WorldDetails.module.less'


type BasicProps = {
  entityIndex: EntityIndex|undefined;
};

export const BasicInfo = ({entityIndex}:BasicProps) => {
  const {
    components: { Agent },
  } = useMUD();

  const agentInfo = useComponentValue(Agent, entityIndex);

  return agentInfo ? (
    <div className={styles.basic_info}>
      <h1 className={styles.agent_title}>Agent Details</h1>
      <h2 className={styles.agent_item}>Name: {agentInfo.name}</h2>
      <h2 className={styles.agent_item}>Agen: {agentInfo.age}</h2>
      <h2 className={styles.agent_item}>Occupation: {agentInfo.occupation}</h2>
      <h2 className={styles.agent_item}>Model: {agentInfo.model}</h2>
    </div>
  ):(
    <div className={styles.basic_info}>
      <h1 className={styles.agent_title}>Agent Details</h1>
      <h2 className={styles.agent_item}>No infos</h2>
    </div>
  )
};

type StatusProps = {
  entityIndex: EntityIndex|undefined;
};

export const StatusInfo = ({entityIndex}:StatusProps) => {
  const {
    components: { Status },
  } = useMUD();

  const statusInfo = useComponentValue(Status, entityIndex);

  return statusInfo ? (
    <div className={styles.basic_info}>
      <h1 className={styles.agent_title}>Current Status</h1>
      <h2 className={styles.agent_item}>{statusInfo.value}</h2>
    </div>
  ):(
    <div className={styles.basic_info}>
      <h1 className={styles.agent_title}>Current Status</h1>
      <h2 className={styles.agent_item}>No status</h2>
    </div>
  )
};

type PlanProps = {
  entityIndex: EntityIndex|undefined;
};

export const PlanInfo = ({entityIndex}:PlanProps) => {
  const {
    components: { Plan },
  } = useMUD();

  const planInfo = useComponentValue(Plan, entityIndex);

  return planInfo ? (
    <div className={styles.basic_info}>
      <h1 className={styles.agent_title}>Current Plan</h1>
      <h2 className={styles.agent_item}>{planInfo.value}</h2>
    </div>
  ):(
    <div className={styles.basic_info}>
      <h1 className={styles.agent_title}>Current Plan</h1>
      <h2 className={styles.agent_item}>No plan</h2>
    </div>
  )
};

type PositionProps = {
  entityIndex: EntityIndex|undefined;
};

export const PositionInfo = ({entityIndex}:PositionProps) => {
  const {
    components: { Position },
  } = useMUD();

  const positionInfo = useComponentValue(Position, entityIndex);

  return positionInfo ? (
    <div className={styles.basic_info}>
      <h1 className={styles.agent_title}>Current Position</h1>
      <h2 className={styles.agent_item}>(x: {positionInfo.x}, y: {positionInfo.x}) </h2>
    </div>
  ):(
    <div className={styles.basic_info}>
      <h1 className={styles.agent_title}>Current Position</h1>
      <h2 className={styles.agent_item}>No position</h2>
    </div>
  )
};

type ChatProps = {
  entityIndex: EntityIndex|undefined;
};

export const ChatInfo = ({ entityIndex }: ChatProps) => {
  const {
    components: { Agent, Chat },
  } = useMUD();

  let [chats, setChats] = useState<Array<string>>([]);

  const agentInfo = useComponentValue(Agent, entityIndex);
  const chatInfo = useComponentValue(Chat, entityIndex);

  const loadChats = async (name: string) => {
    let data = {
      name: name
    }
    let url = config.aiServiceUrl + "/api/mud.ChatLogs"
    console.log("loadChats url:" + url);
    console.log("loadChats data:", data);

    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
  
    let resp = await response.json() as any;
    console.log("loadChats resp:", resp);

    let chats = [];

    if (resp && resp.logs) {
      for (let i=0; i<resp.logs.length; i++) {
        let log = resp.logs[i];
        
        chats.push(log.source + ": " + log.content)
      }
    }

    return chats
  }

  useEffect(() => {
    if (agentInfo) {
      loadChats(agentInfo.name).then((chats)=>{
        console.log("agent:", agentInfo.name, ", chats:", chats);

        setChats(chats)
      })
    }
  }, [entityIndex, agentInfo, chatInfo]);

  return (
    <div className={styles.chat_info}>
      <h1 className={styles.chat_title}>Current conversation</h1>
      <div className={styles.chat_box}>
        {chats &&
          chats.length > 0 ?
          chats.map((item: string, index: number) => {
            return (
              <h2 key={"chat_item_" + index} className={styles.chat_item}>{item}</h2>
            )
          }) : (
            <h2 className={styles.chat_item}>No conversations</h2>
          )
        }
      </div>
    </div>
  )
};

type AgentProps = {
  entityIndex: EntityIndex|undefined;
};

export const AgentInfo = ({ entityIndex }: AgentProps) => {
  const {
    components: { Agent },
  } = useMUD();

  const agentInfo = useComponentValue(Agent, entityIndex);

  return agentInfo ? (
    <div className={styles.agent_info}>
      <BasicInfo entityIndex={entityIndex}></BasicInfo>
      <StatusInfo entityIndex={entityIndex}></StatusInfo>
      <PlanInfo entityIndex={entityIndex}></PlanInfo>
      <PositionInfo entityIndex={entityIndex}></PositionInfo>
      <ChatInfo entityIndex={entityIndex}></ChatInfo>
    </div>
  ):(
    <div className={styles.agent_info}>
      <h1 className={styles.agent_title}>Agent Details</h1>
      <h2 className={styles.agent_item}>No infos</h2>
    </div>
  )
};



export const WorldInfo = () => {
  return (
    <div className={styles.world_info}>
      <h1 className={styles.world_name}>Anyoung AItown</h1>
      <h2 className={styles.world_desc}>Anyoung AItown is An interactive sandbox game.Merge techs like openai-gpt4,latticexyz-mud to create a world for ai agents and allow human players to give prompt to agents.</h2>
    </div>
  );
};

type WorldDetailProps = {
  world: World|undefined;
};

export const WorldDetails = ({ world }: WorldDetailProps) => {
  let [selectedEntity, setSelectedEntity] = useState<EntityIndex|undefined>(undefined);

  useEffect(() => {
    const onEntitySelecetd = (_e: any)=>{
      setSelectedEntity(world?.SelectedEntity)
    }

    world?.on("entity_selected", onEntitySelecetd)
    if (world?.SelectedEntity) {
      setSelectedEntity(world?.SelectedEntity)
    }

    return () => {
      world?.off("entity_selected", onEntitySelecetd)
    };
  }, [world]);

  return (
    <div className={styles.world_details}>
      {
        selectedEntity ? (
          <AgentInfo entityIndex={world?.SelectedEntity}></AgentInfo>
        ):(
          <WorldInfo></WorldInfo>
        )
      }
    </div>
  );
};
