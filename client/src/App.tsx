import { SyncState } from "@latticexyz/network";
import { useComponentValue } from "@latticexyz/react";
import { useMUD } from "./MUDContext";
import MainScene from "./scenes/MainScene";
import { World } from "./world/World";

import styles from './App.module.less'
import { useState } from "react";
import { WorldDetails } from "./WorldDetails";

function timestampToDate(timestampInSeconds: number): Date {
  const timestampInMilliseconds = timestampInSeconds * 1000;
  const date = new Date(timestampInMilliseconds);
  return date;
}

function formatDate(date: Date): string {
  const day = date.getDate();
  const month = date.getMonth() + 1;
  const year = date.getFullYear();
  const hours = date.getHours();
  const minutes = date.getMinutes();
  const seconds = date.getSeconds();
  const amPm = hours >= 12 ? 'PM' : 'AM';

  const formattedDate = `${day.toString().padStart(2, '0')}/${month.toString().padStart(2, '0')}/${year} ${((hours + 11) % 12) + 1}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')} ${amPm}`;

  return formattedDate;
}

export const App = () => {
  const {
    components: { LoadingState, TimeAware },
    singletonEntity,
  } = useMUD();

  const [world, setWorld] = useState<World|undefined>(undefined);

  const loadingState = useComponentValue(LoadingState, singletonEntity, {
    state: SyncState.CONNECTING,
    msg: "Connecting",
    percentage: 0,
  });

  const currentTime = useComponentValue(TimeAware, singletonEntity);

  const readyFunc = (world: World)=>{
    setWorld(world)
  }

  return (
    <div className={styles.container}>
      <div className={styles.left}>
        <div className={styles.gameHeader}>
          <div className={styles.logo}>
            <span className={styles.logo_left}>Anyoung</span> <span className={styles.logo_right}>AItown</span>
          </div>
          <div className={styles.head2}>
            <div className={styles.head2_left}>
              <svg width="20" height="16" viewBox="0 0 20 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M20 1.89414C19.2642 2.21529 18.4736 2.43237 17.6435 2.52979C18.4904 2.02992 19.1413 1.2383 19.4473 0.295577C18.6546 0.758374 17.7762 1.09486 16.8419 1.27538C16.0937 0.490923 15.0272 0 13.847 0C11.5811 0 9.74378 1.80823 9.74378 4.03938C9.74378 4.35566 9.78014 4.66428 9.85027 4.96011C6.44001 4.79161 3.41675 3.18333 1.39293 0.739197C1.0397 1.33598 0.83737 2.03017 0.83737 2.77014C0.83737 4.17157 1.56176 5.40757 2.66275 6.13219C1.99031 6.11097 1.35761 5.92917 0.804384 5.62695C0.803865 5.64383 0.803865 5.66044 0.803865 5.67783C0.803865 7.63436 2.2181 9.26694 4.09491 9.63845C3.75076 9.73025 3.38844 9.77985 3.01417 9.77985C2.7495 9.77985 2.49263 9.75479 2.24199 9.70749C2.76405 11.3119 4.27931 12.4802 6.07483 12.5129C4.67047 13.596 2.90145 14.2421 0.978923 14.2421C0.647767 14.2421 0.321286 14.2232 0 14.1856C1.81577 15.3316 3.97257 16 6.28963 16C13.8369 16 17.964 9.84531 17.964 4.50805C17.964 4.33316 17.9598 4.15853 17.952 3.98491C18.7543 3.41575 19.4502 2.70417 20 1.89414Z" fill="white"/>
              </svg>
              <span>@anyoung_AItown</span>
            </div>
            <div className={styles.head2_right}>
              {
                currentTime ? (
                  "Current time: " + formatDate(timestampToDate(currentTime.value))
                ):
                "Current time: No Time"
              }
            </div>
          </div>
        </div>
        <div className={styles.gameBody}>
          {loadingState.state !== SyncState.LIVE ? (
            <div className={styles.loading}>
              <div className={styles.text}>{loadingState.msg} ({Math.floor(loadingState.percentage)}%)</div>
            </div>
          ) : (
            <MainScene ready={readyFunc}/>
          )}
        </div>
      </div>
      <div className={styles.right}>
        <WorldDetails world={world}></WorldDetails>
      </div>
    </div>
  );
};
