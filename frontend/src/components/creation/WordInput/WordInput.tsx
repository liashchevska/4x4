import styles from "./WordInput.module.css";

type WordInputProps = {
  text: string;
  onTextChange: (value: string) => void;
};

export function WordInput({ text, onTextChange }: WordInputProps) {
  return (
    <input
      aria-labelledby="words-list"
      className={styles.input}
      type="text"
      value={text}
      onChange={(e) => onTextChange(e.target.value)}
    />
  );
}
