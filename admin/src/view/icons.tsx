import React from "react";

export const LockIcon = () => {
  return (
    <span className="absolute top-2.5 left-3">
      <i className="mdi mdi-lock-alert-outline text-2xl" />
    </span>
  );
};

export const ProfileIcon = () => {
  return (
    <span className="absolute top-2.5 left-3">
      <i className="mdi mdi-account-outline text-2xl" />
    </span>
  );
};

export const EmailIcon = () => {
  return (
    <span className="absolute top-2.5 left-3">
      <i className="mdi mdi-email-outline text-2xl" />
    </span>
  );
};

export const GreenBadge = (props: { label: string }) => {
  return (
    <p className="bg-success bg-opacity-10 text-success inline-flex rounded-full px-3 py-1 text-sm font-medium">
      {props.label}
    </p>
  );
};

export const RedBadge = (props: { label: string }) => {
  return (
    <p className="bg-danger bg-opacity-10 text-danger inline-flex rounded-full px-3 py-1 text-sm font-medium">
      {props.label}
    </p>
  );
};

export const YellowBadge = (props: { label: string }) => {
  return (
    <p className="bg-warning bg-opacity-10 text-warning inline-flex rounded-full px-3 py-1 text-sm font-medium">
      {props.label}
    </p>
  );
};

export const Settings = () => {
  return (
    <i className="mdi mdi-code-json text-xl" />
  );
}
